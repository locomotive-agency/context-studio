from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from ..auth import current_user
from ..cms import ContentStore


def build_router(
    get_content: Callable[[], ContentStore],
    prepare_write: Callable[[dict, list[str]], dict],
    finish_write: Callable[[dict], None],
) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/documents")
    def list_documents(user: dict = Depends(current_user)) -> list[dict]:
        return get_content().list_documents()

    @router.post("/documents/move")
    def move_document(data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            result = get_content().move_document(data.get("path", ""), data.get("target_folder", ""), user["username"])
            finish_write(user)
            return result
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (FileExistsError, ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/documents/{document_path:path}")
    def get_document(document_path: str, user: dict = Depends(current_user)) -> dict:
        try:
            return get_content().read_document(document_path)
        except (FileNotFoundError, ValueError) as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.put("/documents/{document_path:path}")
    def save_document(document_path: str, data: dict, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            result = get_content().save_document(
                document_path,
                data.get("frontmatter", {}),
                data.get("body", ""),
                user["username"],
            )
            finish_write(user)
            return result
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.delete("/documents/{document_path:path}")
    def delete_document(document_path: str, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["editor", "admin"])
        try:
            get_content().delete_document(document_path, user["username"])
            finish_write(user)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"status": "deleted"}

    return router
