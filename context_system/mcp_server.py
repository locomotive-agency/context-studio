from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import get_config
from .mcp_tools import execute_mcp_tool
from .request_context import mcp_user_or_service_account
from .service import ContextService

service = ContextService()
mcp = FastMCP(
    get_config().context_server_name,
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)


@mcp.tool()
def list_context_scopes() -> list[dict]:
    """List governed context scope nodes."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "list_context_scopes")


@mcp.tool()
def list_context_types(scope_id: str | None = None) -> list[str]:
    """List context document types visible for the optional scope."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "list_context_types", {"scope_id": scope_id})


@mcp.tool()
def list_context_folders(type: str | None = None, scope_id: str | None = None) -> list[dict]:
    """List context folders containing visible documents, optionally filtered by type and scope."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "list_context_folders", {"type": type, "scope_id": scope_id})


@mcp.tool()
def read_context_index(folder: str | None = None, scope_id: str | None = None) -> dict:
    """Read a context folder index document."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "read_context_index", {"folder": folder, "scope_id": scope_id})


@mcp.tool()
def read_context_log(folder: str | None = None, scope_id: str | None = None) -> dict:
    """Read a context folder log document."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "read_context_log", {"folder": folder, "scope_id": scope_id})


@mcp.tool()
def list_context_documents(
    type: str,
    scope_id: str | None = None,
    folder: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """List visible context document metadata without body text."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(
        service,
        "list_context_documents",
        {"type": type, "scope_id": scope_id, "folder": folder, "limit": limit},
    )


@mcp.tool()
def read_context_document(path: str, scope_id: str | None = None) -> dict:
    """Read the full text for one visible context document."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "read_context_document", {"path": path, "scope_id": scope_id})


@mcp.tool()
def search_collection(collection: str, query: str, limit: int = 10) -> list[dict]:
    """Search a supporting Collection discovered from scoped context metadata."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "search_collection", {"collection": collection, "query": query, "limit": limit})


@mcp.tool()
def read_collection_source(collection: str, source_id: str) -> dict:
    """Read a Collection source discovered from collection search results."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "read_collection_source", {"collection": collection, "source_id": source_id})


@mcp.tool()
def validate_context() -> dict:
    """Return context validation failures."""
    mcp_user_or_service_account(service.config)
    return execute_mcp_tool(service, "validate_context")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
