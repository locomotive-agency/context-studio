from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import get_config
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
    return service.get_construct(construct, scope_id=scope_id)


@mcp.tool()
def search_context(query: str, constructs: list[str] | None = None, top_k: int = 5) -> list[dict]:
    """Search valid hybrid and flexible context documents."""
    return service.search(query=query, constructs=constructs, top_k=top_k)


@mcp.tool()
def assemble_context_package(task: str, constructs: list[str], icp: str | None = None) -> dict:
    """Assemble governed context for an AI task."""
    return service.assemble_context_package(task=task, constructs=constructs, icp=icp).to_response()


@mcp.tool()
def validate_context_bundle() -> dict:
    """Return OKF validation failures in the context bundle."""
    return service.repository.content.validation_report()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
