from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from ..auth import current_user
from ..cms import ContentStore
from ..service import ContextService


def build_router(
    get_content: Callable[[], ContentStore],
    get_service: Callable[[], ContextService],
    prepare_write: Callable[[dict, list[str]], dict],
    finish_write: Callable[[dict], None],
) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/folders")
    def list_folders(user: dict = Depends(current_user)) -> list[dict]:
        return get_content().list_folders()

    @router.get("/scopes")
    def list_scopes(user: dict = Depends(current_user)) -> list[dict]:
        return get_content().list_scopes()

    @router.post("/scopes")
    def create_scope(data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        try:
            result = get_content().save_scope(data, user["username"])
            finish_write(user)
            return result
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/scopes/reorder")
    def reorder_scopes(data: dict, user: dict = Depends(current_user)) -> list[dict]:
        user = prepare_write(user, ["admin"])
        ordered_ids = data.get("ordered_ids", [])
        if not isinstance(ordered_ids, list):
            raise HTTPException(status_code=400, detail="ordered_ids must be a list")
        try:
            result = get_content().reorder_scopes(data.get("parent_id"), ordered_ids, user["username"])
            finish_write(user)
            return result
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/scopes/move")
    def move_scope(data: dict, user: dict = Depends(current_user)) -> list[dict]:
        user = prepare_write(user, ["admin"])
        try:
            result = get_content().move_scope(
                scope_id=data.get("scope_id", ""),
                parent_id=data.get("parent_id") or None,
                index=int(data.get("index", 0)),
                author=user["username"],
            )
            finish_write(user)
            return result
        except (TypeError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.patch("/scopes/{scope_id}")
    def update_scope(scope_id: str, data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        try:
            result = get_content().save_scope(data, user["username"], existing_id=scope_id)
            finish_write(user)
            return result
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.delete("/scopes/{scope_id}")
    def delete_scope(scope_id: str, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        try:
            get_content().delete_scope(scope_id, user["username"])
            finish_write(user)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"status": "deleted"}

    @router.post("/folders")
    def create_folder(data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            result = get_content().create_folder(data.get("path", ""), user["username"])
            finish_write(user)
            return result
        except (ValueError, FileExistsError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/folders/move")
    def move_folder(data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            result = get_content().move_folder(data.get("path", ""), data.get("target_parent", ""), user["username"])
            finish_write(user)
            return result
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (FileExistsError, ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.delete("/folders/{folder_path:path}")
    def delete_folder(folder_path: str, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            get_content().delete_folder(folder_path, user["username"])
            finish_write(user)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"status": "deleted"}

    @router.put("/schemas")
    def save_schema(data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        try:
            result = get_content().save_schema(data.get("path", ""), data.get("schema", {}), user["username"])
            finish_write(user)
            return result
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/validation")
    def validation_report(user: dict = Depends(current_user)) -> dict:
        return get_content().validation_report()

    @router.get("/history")
    def history(path: str | None = None, user: dict = Depends(current_user)) -> list[dict]:
        return get_content().git.history(path)

    @router.get("/history/{commit}/diff")
    def diff(commit: str, path: str | None = None, user: dict = Depends(current_user)) -> dict:
        try:
            return {"diff": get_content().git.diff(commit, path)}
        except (OSError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/history/{commit}/restore")
    def restore_revision(commit: str, data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            result = get_content().restore_document(data.get("path", ""), commit, user["username"])
            finish_write(user)
            return result
        except (OSError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/records")
    def list_records(user: dict = Depends(current_user)) -> list[dict]:
        return [record.model_dump() for record in get_service().repository.runtime_records(include_body=False)]

    return router
