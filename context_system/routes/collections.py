from __future__ import annotations

import base64
import binascii
from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from ..api_models import CollectionCreateRequest, CollectionDocumentRequest
from ..auth import current_user, require_role
from ..service import ContextService


def build_router(get_service: Callable[[], ContextService]) -> APIRouter:
    router = APIRouter(prefix="/api/collections")

    @router.get("")
    def list_collections(user: dict = Depends(current_user)) -> list[dict]:
        return get_service().collections.list_collections()

    @router.post("")
    def create_collection(data: CollectionCreateRequest, user: dict = Depends(current_user)) -> dict:
        require_role(user, ["editor", "admin"])
        try:
            return get_service().collections.create_collection(
                data.id or data.name or "",
                data.name or data.id or "",
                data.description,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/{collection_id}/documents")
    def list_collection_documents(collection_id: str, user: dict = Depends(current_user)) -> list[dict]:
        try:
            return get_service().collections.list_documents(collection_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.post("/{collection_id}/documents")
    def add_collection_document(collection_id: str, data: CollectionDocumentRequest, user: dict = Depends(current_user)) -> dict:
        require_role(user, ["editor", "admin"])
        filename = data.filename
        if not filename:
            raise HTTPException(status_code=400, detail="filename is required")
        try:
            if data.content_base64:
                encoded = data.content_base64
                if not isinstance(encoded, str):
                    raise HTTPException(status_code=400, detail="content_base64 must be a string")
                try:
                    content = base64.b64decode(encoded, validate=True)
                except (binascii.Error, ValueError) as exc:
                    raise HTTPException(status_code=400, detail="content_base64 must be valid base64") from exc
                return get_service().collections.add_document_bytes(collection_id, filename, content)
            if not isinstance(data.content, str):
                raise HTTPException(status_code=400, detail="content must be a string")
            return get_service().collections.add_document_text(collection_id, filename, data.content)
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return router
