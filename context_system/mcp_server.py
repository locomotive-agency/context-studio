from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import get_config
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
def get_construct(construct: str, scope_id: str | None = None) -> list[dict]:
    """Return approved OKF context documents for a construct."""
    mcp_user_or_service_account(service.config)
    return service.get_construct(construct, scope_id=scope_id)


@mcp.tool()
def assemble_context_package(
    task: str,
    requests: list[dict],
    scope_id: str | None = None,
    run_id: str | None = None,
) -> dict:
    """Assemble governed context for an AI task."""
    user = mcp_user_or_service_account(service.config)
    return service.assemble_context_package(task=task, scope_id=scope_id, requests=requests, run_id=run_id, user=user)


@mcp.tool()
def list_okf_bundle(folder: str | None = None) -> list[dict]:
    """List OKF entries, including index and log files, for a folder."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.list_okf_entries(folder)


@mcp.tool()
def read_okf_document(path: str) -> dict:
    """Read an OKF concept, index, or log document."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.read_okf_entry(path)


@mcp.tool()
def read_okf_index(folder: str | None = None) -> dict:
    """Read an OKF index document."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.read_okf_index(folder)


@mcp.tool()
def read_okf_log(folder: str | None = None) -> dict:
    """Read an OKF log document."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.read_okf_log(folder)


@mcp.tool()
def list_okf_types(scope_id: str | None = None) -> list[str]:
    """List approved OKF types discoverable for the optional scope."""
    mcp_user_or_service_account(service.config)
    types = {record.type for record in service.repository.runtime_records(include_body=False)}
    for folder in service.repository.content.list_folders():
        value = folder["effective_schema"].get("type")
        if isinstance(value, str) and value:
            types.add(value)
    if scope_id:
        types = {type_name for type_name in types if service.repository.get_construct(type_name, include_body=False, scope_id=scope_id) or service.repository.resolve_criticality(type_name, scope_id=scope_id)}
    return sorted(types)


@mcp.tool()
def list_okf_scopes() -> list[dict]:
    """List OKF scope nodes."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.list_scopes()


@mcp.tool()
def validate_context_bundle() -> dict:
    """Return OKF validation failures in the context bundle."""
    mcp_user_or_service_account(service.config)
    return service.repository.content.validation_report()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
