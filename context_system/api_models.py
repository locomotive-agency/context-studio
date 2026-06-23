from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator


class MCPToolRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}

    @model_validator(mode="before")
    @classmethod
    def _use_body_as_payload(cls, value: Any) -> dict[str, Any]:
        if value is None:
            return {"payload": {}}
        if isinstance(value, dict) and set(value) == {"payload"} and isinstance(value["payload"], dict):
            return value
        if isinstance(value, dict):
            return {"payload": value}
        raise ValueError("request body must be a JSON object")


class OKFFolderPathRequest(BaseModel):
    source_folder: str = ""

    model_config = {"extra": "forbid"}


class UploadedFileRequest(BaseModel):
    path: str
    content_base64: str | None = None
    content: str | None = None

    model_config = {"extra": "forbid"}


class UploadedOKFFolderRequest(BaseModel):
    folder_name: str = ""
    files: list[UploadedFileRequest] = Field(default_factory=list)

    model_config = {"extra": "forbid"}

    def files_payload(self) -> list[dict]:
        return [file.model_dump(exclude_none=True) for file in self.files]


class CollectionCreateRequest(BaseModel):
    id: str | None = None
    name: str | None = None
    description: str = ""

    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def _require_identifier(self) -> "CollectionCreateRequest":
        if not (self.id or self.name):
            raise ValueError("id or name is required")
        return self


class CollectionDocumentRequest(BaseModel):
    filename: str
    content_base64: Any | None = None
    content: Any | None = ""

    model_config = {"extra": "forbid"}
