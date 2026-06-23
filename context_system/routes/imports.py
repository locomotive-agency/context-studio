from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException

from ..api_models import OKFFolderPathRequest, UploadedOKFFolderRequest
from ..auth import current_user, require_role
from ..service import ContextService


def build_router(
    get_service: Callable[[], ContextService],
    prepare_write: Callable[[dict, list[str]], dict],
    finish_write: Callable[[dict], None],
) -> APIRouter:
    router = APIRouter(prefix="/api/imports")

    @router.post("/okf-folder/scan")
    def scan_okf_folder(data: OKFFolderPathRequest, user: dict = Depends(current_user)) -> dict:
        require_role(user, ["admin"])
        source_folder = data.source_folder
        if not source_folder:
            raise HTTPException(status_code=400, detail="source_folder is required")
        return get_service().scan_okf_folder(source_folder)

    @router.post("/okf-folder/apply")
    def apply_okf_folder_import(data: OKFFolderPathRequest, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        source_folder = data.source_folder
        if not source_folder:
            raise HTTPException(status_code=400, detail="source_folder is required")
        try:
            result = get_service().import_okf_folder(source_folder, user["username"])
            finish_write(user)
            return result
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/okf-folder/scan-upload")
    def scan_uploaded_okf_folder(data: UploadedOKFFolderRequest, user: dict = Depends(current_user)) -> dict:
        require_role(user, ["admin"])
        try:
            return get_service().scan_uploaded_okf_folder(data.folder_name, data.files_payload())
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.post("/okf-folder/apply-upload")
    def apply_uploaded_okf_folder(data: UploadedOKFFolderRequest, user: dict = Depends(current_user)) -> dict:
        user = prepare_write(user, ["admin"])
        try:
            result = get_service().import_uploaded_okf_folder(data.folder_name, data.files_payload(), user["username"])
            finish_write(user)
            return result
        except (ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return router
