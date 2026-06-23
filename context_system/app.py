from __future__ import annotations

from contextlib import asynccontextmanager
from subprocess import CalledProcessError

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from .auth import GitHubAuth, UserStore, current_user, require_role
from .cms import ContentStore
from .config import get_config
from .mcp_server import mcp
from .request_context import clear_request_user, set_request_user
from .routes import auth as auth_routes
from .routes import collections as collection_routes
from .routes import context_admin as context_admin_routes
from .routes import documents as document_routes
from .routes import imports as import_routes
from .routes import mcp_tools as mcp_tool_routes
from .service import ContextService

cfg = get_config()
service = ContextService(cfg)
content = ContentStore(cfg.context_repo)
users = UserStore(config=cfg)
github_auth = GitHubAuth()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if cfg.github_enabled:
        try:
            content.git.sync_with_remote()
        except CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "Git sync failed").strip()
            raise RuntimeError(detail) from exc
    async with mcp.session_manager.run():
        yield


app = FastAPI(title="Context Studio", version="0.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def request_validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse({"detail": exc.errors()}, status_code=400)


def _public_user(user: dict) -> dict:
    return {
        "username": user["username"],
        "role": user["role"],
        "provider": user.get("provider", "local"),
        "permission": user.get("permission"),
        "auth_mode": "github" if cfg.github_enabled else "local",
        "can_edit": user["role"] in {"editor", "admin"},
    }


def _prepare_write(user: dict, local_roles: list[str]) -> dict:
    if user.get("provider") == "github":
        refreshed = github_auth.refresh_user_permission(user, users)
        require_role(refreshed, local_roles)
        try:
            content.git.sync_with_remote()
        except CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "Git sync failed").strip()
            raise HTTPException(status_code=409, detail=detail) from exc
        return refreshed
    require_role(user, local_roles)
    return user


def _finish_write(user: dict) -> None:
    if user.get("provider") != "github":
        return
    try:
        content.git.push_to_remote()
    except CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "Git push failed").strip()
        raise HTTPException(status_code=409, detail=detail) from exc


@app.middleware("http")
async def require_login_for_mcp(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        token = None
        try:
            user = await current_user(request)
            token = set_request_user(_public_user(user))
        except HTTPException as exc:
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        try:
            return await call_next(request)
        finally:
            clear_request_user(token)
    return await call_next(request)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": cfg.context_server_name, "mcp_url": "/mcp/"}


@app.get("/api/stats")
def stats(user: dict = Depends(current_user)) -> dict:
    return service.stats()


app.include_router(auth_routes.build_router(cfg, users, github_auth, _public_user))
app.include_router(document_routes.build_router(lambda: content, _prepare_write, _finish_write))
app.include_router(context_admin_routes.build_router(lambda: content, lambda: service, _prepare_write, _finish_write))
app.include_router(import_routes.build_router(lambda: service, _prepare_write, _finish_write))
app.include_router(collection_routes.build_router(lambda: service))
app.include_router(mcp_tool_routes.build_router(lambda: service))

app.mount("/mcp", mcp.streamable_http_app())

static_dir = cfg.path("cms/dist")


@app.api_route(
    "/api/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    include_in_schema=False,
)
def unknown_api_route(full_path: str):
    raise HTTPException(status_code=404, detail=f"Unknown API route: /api/{full_path}")


@app.get("/{full_path:path}", include_in_schema=False)
def cms_fallback(full_path: str):
    if not static_dir.is_dir():
        raise HTTPException(status_code=404, detail="CMS build not found")
    requested = (static_dir / full_path).resolve()
    if full_path and requested.is_file() and requested.is_relative_to(static_dir.resolve()):
        return FileResponse(requested)
    index = static_dir / "index.html"
    if index.is_file():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="CMS build not found")
