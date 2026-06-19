from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from .auth import UserStore, current_user, login_response, require_role
from .cms import ContentStore
from .config import get_config
from .mcp_server import mcp
from .service import ContextService

cfg = get_config()
service = ContextService(cfg)
content = ContentStore(cfg.context_repo)
users = UserStore(cfg.users_db)


@asynccontextmanager
async def lifespan(_app: FastAPI):
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


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": cfg.context_server_name, "mcp_url": "/mcp/"}


@app.get("/api/stats")
def stats() -> dict:
    return service.stats()


@app.post("/api/auth/login")
def login(data: dict, response: Response) -> dict:
    username, password = data.get("username", ""), data.get("password", "")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password are required")
    return login_response(username, password, response, users)


@app.get("/api/auth/me")
def me(user: dict = Depends(current_user)) -> dict:
    return user


@app.get("/api/users")
def list_users(user: dict = Depends(current_user)) -> list[dict]:
    require_role(user, ["admin"])
    return users.list_users()


@app.post("/api/users")
def create_user(data: dict, user: dict = Depends(current_user)) -> dict:
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
    require_role(user, ["editor", "admin"])
    try:
        return content.save_document(document_path, data.get("frontmatter", {}), data.get("body", ""), user["username"])
    except (ValueError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/folders")
def list_folders(user: dict = Depends(current_user)) -> list[dict]:
    return content.list_folders()


@app.get("/api/scopes")
def list_scopes(user: dict = Depends(current_user)) -> list[dict]:
    return content.list_scopes()


@app.post("/api/scopes")
def create_scope(data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["admin"])
    try:
        return content.save_scope(data, user["username"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/scopes/reorder")
def reorder_scopes(data: dict, user: dict = Depends(current_user)) -> list[dict]:
    require_role(user, ["admin"])
    ordered_ids = data.get("ordered_ids", [])
    if not isinstance(ordered_ids, list):
        raise HTTPException(status_code=400, detail="ordered_ids must be a list")
    try:
        return content.reorder_scopes(data.get("parent_id"), ordered_ids, user["username"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/scopes/move")
def move_scope(data: dict, user: dict = Depends(current_user)) -> list[dict]:
    require_role(user, ["admin"])
    try:
        return content.move_scope(
            scope_id=data.get("scope_id", ""),
            parent_id=data.get("parent_id") or None,
            index=int(data.get("index", 0)),
            author=user["username"],
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch("/api/scopes/{scope_id}")
def update_scope(scope_id: str, data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["admin"])
    try:
        return content.save_scope(data, user["username"], existing_id=scope_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/scopes/{scope_id}")
def delete_scope(scope_id: str, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["admin"])
    try:
        content.delete_scope(scope_id, user["username"])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "deleted"}


@app.post("/api/folders")
def create_folder(data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["editor", "admin"])
    try:
        return content.create_folder(data.get("path", ""), user["username"])
    except (ValueError, FileExistsError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.put("/api/schemas")
def save_schema(data: dict, user: dict = Depends(current_user)) -> dict:
    require_role(user, ["admin"])
    try:
        return content.save_schema(data.get("path", ""), data.get("schema", {}), user["username"])
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
    require_role(user, ["editor", "admin"])
    try:
        return content.restore_document(data.get("path", ""), commit, user["username"])
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/records")
def list_records(user: dict = Depends(current_user)) -> list[dict]:
    return [record.model_dump() for record in service.repository.runtime_records(include_body=False)]


@app.get("/api/constructs/{construct}")
def get_construct(construct: str, scope_id: str | None = None) -> list[dict]:
    return service.get_construct(construct, scope_id=scope_id)


@app.get("/api/search")
def search_context(query: str, constructs: str | None = None, top_k: int = 5) -> list[dict]:
    construct_list = [item.strip() for item in constructs.split(",") if item.strip()] if constructs else None
    return service.search(query=query, constructs=construct_list, top_k=top_k)


@app.post("/api/assemble_context_package")
def assemble_context_package(data: dict) -> dict:
    task, constructs = data.get("task"), data.get("constructs", [])
    if not task or not isinstance(constructs, list):
        raise HTTPException(status_code=400, detail="task and a constructs list are required")
    return service.assemble_context_package(
        task=task,
        constructs=constructs,
        scope=data.get("scope"),
        icp=data.get("icp"),
        run_id=data.get("run_id"),
        query=data.get("query"),
    ).to_response()


app.mount("/mcp", mcp.streamable_http_app())
