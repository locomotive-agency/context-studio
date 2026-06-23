from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from ..api_models import MCPToolRequest
from ..auth import current_user
from ..mcp_tools import execute_mcp_tool
from ..service import ContextService


def build_router(get_service: Callable[[], ContextService]) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.post("/mcp-tools/{tool_name}")
    def run_mcp_tool(tool_name: str, data: MCPToolRequest, user: dict = Depends(current_user)) -> dict:
        try:
            result = execute_mcp_tool(get_service(), tool_name, data.payload)
            return {"tool": tool_name, "request": data.payload, "result": result}
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="unknown MCP tool") from exc
        except ValidationError as exc:
            raise HTTPException(status_code=400, detail=exc.errors()) from exc
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (PermissionError, ValueError, OSError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return router
