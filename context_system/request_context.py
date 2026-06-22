from __future__ import annotations

from contextvars import ContextVar, Token

from .config import Config

RequestUser = dict[str, str | None]

_request_user: ContextVar[RequestUser | None] = ContextVar("request_user", default=None)


def set_request_user(user: RequestUser) -> Token[RequestUser | None]:
    return _request_user.set(dict(user))


def clear_request_user(token: Token[RequestUser | None] | None = None) -> None:
    if token is None:
        _request_user.set(None)
        return
    _request_user.reset(token)


def current_request_user() -> RequestUser | None:
    return _request_user.get()


def mcp_user_or_service_account(config: Config) -> RequestUser:
    user = current_request_user()
    if user is not None:
        return user
    if config.mcp_service_account_role:
        return {
            "username": "mcp-service-account",
            "role": config.mcp_service_account_role,
            "provider": "service_account",
        }
    raise PermissionError("authenticated MCP user is required")
