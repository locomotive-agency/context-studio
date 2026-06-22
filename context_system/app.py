from __future__ import annotations

import base64
import binascii
from contextlib import asynccontextmanager
from subprocess import CalledProcessError

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .auth import GitHubAuth, UserStore, current_user, login_response, require_role
from .cms import ContentStore
from .config import get_config
from .mcp_server import mcp
from .models import ContextPackageRequest
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


app = FastAPI(title="Context Documentation System", version="0.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        try:
            await current_user(request)
        except HTTPException as exc:
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    return await call_next(request)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": cfg.context_server_name, "mcp_url": "/mcp/"}


@app.get("/api/stats")
def stats(user: dict = Depends(current_user)) -> dict:
    return service.stats()


@app.post("/api/auth/login")
def login(data: dict, response: Response) -> dict:
    if cfg.github_enabled:
        raise HTTPException(status_code=400, detail="Use GitHub to sign in")
    username, password = data.get("username", ""), data.get("password", "")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password are required")
    return login_response(username, password, response, users)


@app.get("/api/auth/config")
def auth_config() -> dict:
    return {"mode": "github" if cfg.github_enabled else "local", "repository": cfg.github_full_name}


@app.get("/api/auth/github/login")
def github_login(request: Request) -> Response:
    return github_auth.login_redirect(request)


@app.get("/api/auth/github/callback")
def github_callback(code: str, state: str, request: Request) -> Response:
    return github_auth.callback_response(code, state, request, users)


@app.get("/api/auth/me")
def me(user: dict = Depends(current_user)) -> dict:
    return _public_user(user)


@app.get("/api/users")
def list_users(user: dict = Depends(current_user)) -> list[dict]:
    if cfg.github_enabled:
        raise HTTPException(status_code=400, detail="User access is managed in GitHub")
    require_role(user, ["admin"])
    return users.list_users()


@app.post("/api/users")
def create_user(data: dict, user: dict = Depends(current_user)) -> dict:
    if cfg.github_enabled:
        raise HTTPException(status_code=400, detail="User access is managed in GitHub")
    require_role(user, ["admin"])
    try:
        created = users.create_user(data.get("username", ""), data.get("password", ""), data.get("role", "viewer"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not created:
        raise HTTPException(status_code=400, detail="user already exists")
    return {"status": "created"}


@app.patch("/api/users/{username}")
def update_user_role(username: str, data: dict, user: dict = Depends(current_user)) -> dict:
    if cfg.github_enabled:
        raise HTTPException(status_code=400, detail="User access is managed in GitHub")
    require_role(user, ["admin"])
    try:
        updated = users.update_user(username, data.get("role", ""), data.get("password") or None)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not updated:
        raise HTTPException(status_code=404, detail="user not found")
    return {"status": "updated"}


@app.delete("/api/users/{username}")
def delete_user(username: str, user: dict = Depends(current_user)) -> dict:
    if cfg.github_enabled:
        raise HTTPException(status_code=400, detail="User access is managed in GitHub")
    require_role(user, ["admin"])
    if username == user["username"]:
        raise HTTPException(status_code=400, detail="you cannot remove your own account")
    try:
        deleted = users.delete_user(username)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="user not found")
    return {"status": "deleted"}


@app.get("/api/documents")
def list_documents(user: dict = Depends(current_user)) -> list[dict]:
    return content.list_documents()


@app.get("/api/documents/{document_path:path}")
def get_document(document_path: str, user: dict = Depends(current_user)) -> dict:
    try:
        return content.read_document(document_path)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/api/documents/{document_path:path}")
def save_document(document_path: str, data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["editor", "admin"])
    try:
        result = content.save_document(document_path, data.get("frontmatter", {}), data.get("body", ""), user["username"])
        _finish_write(user)
        return result
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/documents/{document_path:path}")
def delete_document(document_path: str, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["editor", "admin"])
    try:
        content.delete_document(document_path, user["username"])
        _finish_write(user)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "deleted"}


@app.get("/api/folders")
def list_folders(user: dict = Depends(current_user)) -> list[dict]:
    return content.list_folders()


@app.get("/api/scopes")
def list_scopes(user: dict = Depends(current_user)) -> list[dict]:
    return content.list_scopes()


@app.post("/api/scopes")
def create_scope(data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["admin"])
    try:
        result = content.save_scope(data, user["username"])
        _finish_write(user)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/scopes/reorder")
def reorder_scopes(data: dict, user: dict = Depends(current_user)) -> list[dict]:
    user = _prepare_write(user, ["admin"])
    ordered_ids = data.get("ordered_ids", [])
    if not isinstance(ordered_ids, list):
        raise HTTPException(status_code=400, detail="ordered_ids must be a list")
    try:
        result = content.reorder_scopes(data.get("parent_id"), ordered_ids, user["username"])
        _finish_write(user)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/scopes/move")
def move_scope(data: dict, user: dict = Depends(current_user)) -> list[dict]:
    user = _prepare_write(user, ["admin"])
    try:
        result = content.move_scope(
            scope_id=data.get("scope_id", ""),
            parent_id=data.get("parent_id") or None,
            index=int(data.get("index", 0)),
            author=user["username"],
        )
        _finish_write(user)
        return result
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch("/api/scopes/{scope_id}")
def update_scope(scope_id: str, data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["admin"])
    try:
        result = content.save_scope(data, user["username"], existing_id=scope_id)
        _finish_write(user)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/scopes/{scope_id}")
def delete_scope(scope_id: str, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["admin"])
    try:
        content.delete_scope(scope_id, user["username"])
        _finish_write(user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "deleted"}


@app.post("/api/folders")
def create_folder(data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["editor", "admin"])
    try:
        result = content.create_folder(data.get("path", ""), user["username"])
        _finish_write(user)
        return result
    except (ValueError, FileExistsError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/folders/{folder_path:path}")
def delete_folder(folder_path: str, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["editor", "admin"])
    try:
        content.delete_folder(folder_path, user["username"])
        _finish_write(user)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "deleted"}


@app.put("/api/schemas")
def save_schema(data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["admin"])
    try:
        result = content.save_schema(data.get("path", ""), data.get("schema", {}), user["username"])
        _finish_write(user)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/validation")
def validation_report(user: dict = Depends(current_user)) -> dict:
    return content.validation_report()


@app.get("/api/history")
def history(path: str | None = None, user: dict = Depends(current_user)) -> list[dict]:
    return content.git.history(path)


@app.get("/api/history/{commit}/diff")
def diff(commit: str, path: str | None = None, user: dict = Depends(current_user)) -> dict:
    try:
        return {"diff": content.git.diff(commit, path)}
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/history/{commit}/restore")
def restore_revision(commit: str, data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["editor", "admin"])
    try:
        result = content.restore_document(data.get("path", ""), commit, user["username"])
        _finish_write(user)
        return result
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/records")
def list_records(user: dict = Depends(current_user)) -> list[dict]:
    return [record.model_dump() for record in service.repository.runtime_records(include_body=False)]


@app.get("/api/constructs/{construct}")
def get_construct(construct: str, scope_id: str | None = None, user: dict = Depends(current_user)) -> list[dict]:
    return service.get_construct(construct, scope_id=scope_id)


@app.get("/api/search")
def search_context(query: str, constructs: str | None = None, top_k: int = 5, user: dict = Depends(current_user)) -> list[dict]:
    construct_list = [item.strip() for item in constructs.split(",") if item.strip()] if constructs else None
    return service.search(query=query, constructs=construct_list, top_k=top_k)


@app.post("/api/context-package")
def context_package(data: ContextPackageRequest, user: dict = Depends(current_user)) -> dict:
    return service.assemble_context_package(
        task=data.task,
        scope_id=data.scope_id,
        requests=[item.model_dump() for item in data.requests],
        run_id=data.run_id,
        user=user,
    )


@app.post("/api/assemble_context_package")
def assemble_context_package(data: dict, user: dict = Depends(current_user)) -> dict:
    if isinstance(data.get("requests"), list):
        return service.assemble_context_package(
            task=data.get("task", ""),
            scope_id=data.get("scope_id"),
            requests=data.get("requests", []),
            run_id=data.get("run_id"),
            user=user,
        )
    task, constructs = data.get("task"), data.get("constructs", [])
    if not task or not isinstance(constructs, list):
        raise HTTPException(status_code=400, detail="task and a constructs list are required")
    return service.assemble_construct_context_package(
        task=task,
        constructs=constructs,
        scope=data.get("scope"),
        icp=data.get("icp"),
        run_id=data.get("run_id"),
        query=data.get("query"),
    ).to_response()


@app.post("/api/imports/okf-folder/scan")
def scan_okf_folder(data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["admin"])
    source_folder = data.get("source_folder", "")
    if not source_folder:
        raise HTTPException(status_code=400, detail="source_folder is required")
    return service.scan_okf_folder(source_folder)


@app.post("/api/imports/okf-folder/apply")
def apply_okf_folder_import(data: dict, user: dict = Depends(current_user)) -> dict:
    user = _prepare_write(user, ["admin"])
    source_folder = data.get("source_folder", "")
    if not source_folder:
        raise HTTPException(status_code=400, detail="source_folder is required")
    try:
        result = service.import_okf_folder(source_folder, user["username"])
        _finish_write(user)
        return result
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/collections")
def list_collections(user: dict = Depends(current_user)) -> list[dict]:
    return service.collections.list_collections()


@app.post("/api/collections")
def create_collection(data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["editor", "admin"])
    try:
        return service.collections.create_collection(
            data.get("id") or data.get("name", ""),
            data.get("name") or data.get("id", ""),
            data.get("description", ""),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/collections/{collection_id}/documents")
def list_collection_documents(collection_id: str, user: dict = Depends(current_user)) -> list[dict]:
    try:
        return service.collections.list_documents(collection_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/collections/{collection_id}/documents")
def add_collection_document(collection_id: str, data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["editor", "admin"])
    filename = data.get("filename", "")
    if not filename:
        raise HTTPException(status_code=400, detail="filename is required")
    try:
        if data.get("content_base64"):
            encoded = data["content_base64"]
            if not isinstance(encoded, str):
                raise HTTPException(status_code=400, detail="content_base64 must be a string")
            try:
                content = base64.b64decode(encoded, validate=True)
            except (binascii.Error, ValueError) as exc:
                raise HTTPException(status_code=400, detail="content_base64 must be valid base64") from exc
            return service.collections.add_document_bytes(collection_id, filename, content)
        content_text = data.get("content", "")
        if not isinstance(content_text, str):
            raise HTTPException(status_code=400, detail="content must be a string")
        return service.collections.add_document_text(collection_id, filename, content_text)
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


app.mount("/mcp", mcp.streamable_http_app())
