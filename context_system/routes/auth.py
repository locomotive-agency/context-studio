from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, Request, Response

from ..auth import GitHubAuth, UserStore, current_user, login_response, require_role
from ..config import Config


def build_router(
    cfg: Config,
    users: UserStore,
    github_auth: GitHubAuth,
    public_user: Callable[[dict], dict],
) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.post("/auth/login")
    def login(data: dict, response: Response) -> dict:
        if cfg.github_enabled:
            raise HTTPException(status_code=400, detail="Use GitHub to sign in")
        username, password = data.get("username", ""), data.get("password", "")
        if not username or not password:
            raise HTTPException(status_code=400, detail="username and password are required")
        return login_response(username, password, response, users)

    @router.get("/auth/config")
    def auth_config() -> dict:
        return {"mode": "github" if cfg.github_enabled else "local", "repository": cfg.github_full_name}

    @router.get("/auth/github/login")
    def github_login(request: Request) -> Response:
        return github_auth.login_redirect(request)

    @router.get("/auth/github/callback")
    def github_callback(code: str, state: str, request: Request) -> Response:
        return github_auth.callback_response(code, state, request, users)

    @router.get("/auth/me")
    def me(user: dict = Depends(current_user)) -> dict:
        return public_user(user)

    @router.get("/users")
    def list_users(user: dict = Depends(current_user)) -> list[dict]:
        if cfg.github_enabled:
            raise HTTPException(status_code=400, detail="User access is managed in GitHub")
        require_role(user, ["admin"])
        return users.list_users()

    @router.post("/users")
    def create_user(data: dict, user: dict = Depends(current_user)) -> dict:
        if cfg.github_enabled:
            raise HTTPException(status_code=400, detail="User access is managed in GitHub")
        require_role(user, ["admin"])
        try:
            created = users.create_user(data.get("username", ""), data.get("password", ""), data.get("role", "viewer"))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not created:
            raise HTTPException(status_code=400, detail="user already exists")
        return {"status": "created"}

    @router.patch("/users/{username}")
    def update_user_role(username: str, data: dict, user: dict = Depends(current_user)) -> dict:
        if cfg.github_enabled:
            raise HTTPException(status_code=400, detail="User access is managed in GitHub")
        require_role(user, ["admin"])
        try:
            updated = users.update_user(username, data.get("role", ""), data.get("password") or None)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not updated:
            raise HTTPException(status_code=404, detail="user not found")
        return {"status": "updated"}

    @router.delete("/users/{username}")
    def delete_user(username: str, user: dict = Depends(current_user)) -> dict:
        if cfg.github_enabled:
            raise HTTPException(status_code=400, detail="User access is managed in GitHub")
        require_role(user, ["admin"])
        if username == user["username"]:
            raise HTTPException(status_code=400, detail="you cannot remove your own account")
        try:
            deleted = users.delete_user(username)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not deleted:
            raise HTTPException(status_code=404, detail="user not found")
        return {"status": "deleted"}

    return router
