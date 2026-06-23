from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

from .service import ContextService


class EmptyRequest(BaseModel):
    model_config = {"extra": "forbid"}


class ScopeRequest(BaseModel):
    scope_id: str | None = None

    model_config = {"extra": "forbid"}


class ListContextFoldersRequest(BaseModel):
    type: str | None = None
    scope_id: str | None = None

    model_config = {"extra": "forbid"}


class FolderRequest(BaseModel):
    folder: str | None = None
    scope_id: str | None = None

    model_config = {"extra": "forbid"}


class ListContextDocumentsRequest(BaseModel):
    type: str = ""
    scope_id: str | None = None
    folder: str | None = None
    limit: int = Field(default=100, ge=0)

    model_config = {"extra": "forbid"}


class ReadContextDocumentRequest(BaseModel):
    path: str
    scope_id: str | None = None

    model_config = {"extra": "forbid"}


class SearchCollectionRequest(BaseModel):
    collection: str
    query: str
    limit: int = Field(default=10, ge=0)

    model_config = {"extra": "forbid"}


class ReadCollectionSourceRequest(BaseModel):
    collection: str
    source_id: str

    model_config = {"extra": "forbid"}


ToolRunner = Callable[[ContextService, BaseModel], Any]


class ToolDefinition(BaseModel):
    request_model: type[BaseModel]
    runner: ToolRunner

    model_config = {"arbitrary_types_allowed": True}


MCP_TOOLS: dict[str, ToolDefinition] = {
    "list_context_scopes": ToolDefinition(
        request_model=EmptyRequest,
        runner=lambda service, request: service.list_context_scopes(),
    ),
    "list_context_types": ToolDefinition(
        request_model=ScopeRequest,
        runner=lambda service, request: service.list_context_types(scope_id=request.scope_id),
    ),
    "list_context_folders": ToolDefinition(
        request_model=ListContextFoldersRequest,
        runner=lambda service, request: service.list_context_folders(type=request.type, scope_id=request.scope_id),
    ),
    "read_context_index": ToolDefinition(
        request_model=FolderRequest,
        runner=lambda service, request: service.read_context_index(folder=request.folder, scope_id=request.scope_id),
    ),
    "read_context_log": ToolDefinition(
        request_model=FolderRequest,
        runner=lambda service, request: service.read_context_log(folder=request.folder, scope_id=request.scope_id),
    ),
    "list_context_documents": ToolDefinition(
        request_model=ListContextDocumentsRequest,
        runner=lambda service, request: service.list_context_documents(
            type=request.type,
            scope_id=request.scope_id,
            folder=request.folder,
            limit=request.limit,
        ),
    ),
    "read_context_document": ToolDefinition(
        request_model=ReadContextDocumentRequest,
        runner=lambda service, request: service.read_context_document(path=request.path, scope_id=request.scope_id),
    ),
    "search_collection": ToolDefinition(
        request_model=SearchCollectionRequest,
        runner=lambda service, request: service.search_collection(
            collection=request.collection,
            query=request.query,
            limit=request.limit,
        ),
    ),
    "read_collection_source": ToolDefinition(
        request_model=ReadCollectionSourceRequest,
        runner=lambda service, request: service.read_collection_source(
            collection=request.collection,
            source_id=request.source_id,
        ),
    ),
    "validate_context": ToolDefinition(
        request_model=EmptyRequest,
        runner=lambda service, request: service.validate_context(),
    ),
}


def execute_mcp_tool(service: ContextService, tool_name: str, payload: dict[str, Any] | None = None) -> Any:
    if tool_name not in MCP_TOOLS:
        raise KeyError(tool_name)
    definition = MCP_TOOLS[tool_name]
    request = definition.request_model.model_validate(payload or {})
    return definition.runner(service, request)
