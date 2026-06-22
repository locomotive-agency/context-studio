from __future__ import annotations

import base64
import hashlib
import hmac
import os
import sqlite3
import time
from pathlib import Path
from urllib.parse import quote, urlencode

import httpx
from fastapi import HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from .config import Config, LocalDemoUser, get_config

COOKIE_NAME = "context_system_session"
OAUTH_STATE_COOKIE = "context_system_oauth_state"
ROLES = ("viewer", "editor", "admin")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'editor', 'admin'))
);

CREATE TABLE IF NOT EXISTS oauth_sessions (
    session_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'editor', 'admin')),
    provider TEXT NOT NULL,
    permission TEXT NOT NULL,
    access_token TEXT NOT NULL,
    expires_at INTEGER NOT NULL
);
"""


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()
    return password_hash, salt


class UserStore:
    def __init__(self, db_path: Path | None = None, config: Config | None = None):
        self.config = config or get_config()
        self.db_path = db_path or self.config.users_db
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA)
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if count == 0:
                self._seed_local_demo_users(conn, self.config.local_demo_users)

    @staticmethod
    def _seed_local_demo_users(conn: sqlite3.Connection, users: list[LocalDemoUser]) -> None:
        for user in users:
            password_hash, salt = hash_password(user.password)
            conn.execute(
                "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                (user.username, password_hash, salt, user.role),
            )

    def get_user(self, username: str) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None

    def list_users(self) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT username, role FROM users ORDER BY username").fetchall()
        return [dict(row) for row in rows]

    def create_user(self, username: str, password: str, role: str) -> bool:
        if role not in ROLES:
            raise ValueError(f"role must be one of {ROLES}")
        password_hash, salt = hash_password(password)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                    (username, password_hash, salt, role),
                )
        except sqlite3.IntegrityError:
            return False
        return True

    def update_role(self, username: str, role: str) -> bool:
        if role not in ROLES:
            raise ValueError(f"role must be one of {ROLES}")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
        return cursor.rowcount > 0

    def update_user(self, username: str, role: str, password: str | None = None) -> bool:
        if role not in ROLES:
            raise ValueError(f"role must be one of {ROLES}")
        with sqlite3.connect(self.db_path) as conn:
            current = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
            if not current:
                return False
            if current[0] == "admin" and role != "admin":
                admin_count = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]
                if admin_count == 1:
                    raise ValueError("at least one admin is required")
            if password:
                password_hash, salt = hash_password(password)
                conn.execute(
                    "UPDATE users SET role = ?, password_hash = ?, salt = ? WHERE username = ?",
                    (role, password_hash, salt, username),
                )
            else:
                conn.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))
        return True

    def delete_user(self, username: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            current = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
            if not current:
                return False
            if current[0] == "admin":
                admin_count = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'").fetchone()[0]
                if admin_count == 1:
                    raise ValueError("at least one admin is required")
            cursor = conn.execute("DELETE FROM users WHERE username = ?", (username,))
        return cursor.rowcount > 0

    def create_oauth_session(self, username: str, role: str, provider: str, permission: str, access_token: str) -> str:
        if role not in ROLES:
            raise ValueError(f"role must be one of {ROLES}")
        session_id = os.urandom(24).hex()
        expires_at = int(time.time()) + 86_400
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM oauth_sessions WHERE expires_at < ?", (int(time.time()),))
            conn.execute(
                """
                INSERT INTO oauth_sessions (session_id, username, role, provider, permission, access_token, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (session_id, username, role, provider, permission, access_token, expires_at),
            )
        return session_id

    def get_oauth_session(self, session_id: str) -> dict | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM oauth_sessions WHERE session_id = ?", (session_id,)).fetchone()
            if not row:
                return None
            if row["expires_at"] < int(time.time()):
                conn.execute("DELETE FROM oauth_sessions WHERE session_id = ?", (session_id,))
                return None
        return dict(row)


def create_token(username: str, role: str, provider: str = "local", session_id: str = "") -> str:
    expiry = int(time.time()) + 86_400
    payload = f"{username}:{role}:{provider}:{session_id}:{expiry}"
    payload_b64 = base64.urlsafe_b64encode(payload.encode()).decode()
    signature = hmac.new(get_config().secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"


def verify_token(token: str) -> dict | None:
    try:
        payload_b64, signature = token.split(".", 1)
        expected = hmac.new(get_config().secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        parts = base64.urlsafe_b64decode(payload_b64.encode()).decode().split(":")
        if len(parts) == 3:
            username, role, expiry = parts
            provider, session_id = "local", ""
        elif len(parts) == 5:
            username, role, provider, session_id, expiry = parts
        else:
            return None
        if int(expiry) < time.time():
            return None
        return {"username": username, "role": role, "provider": provider, "session_id": session_id}
    except (ValueError, TypeError):
        return None


def login_response(username: str, password: str, response: Response, users: UserStore) -> dict:
    user = users.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    password_hash, _salt = hash_password(password, user["salt"])
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    response.set_cookie(COOKIE_NAME, create_token(username, user["role"]), httponly=True, samesite="lax")
    return {"username": username, "role": user["role"]}


def github_role_for_permission(permission: str) -> str | None:
    if permission == "admin":
        return "admin"
    if permission in {"write", "maintain"}:
        return "editor"
    if permission in {"read", "triage"}:
        return "viewer"
    return None


class GitHubAuth:
    def __init__(self):
        self.cfg = get_config()

    def enabled(self) -> bool:
        return self.cfg.github_enabled

    def login_redirect(self, request: Request) -> RedirectResponse:
        if not self.enabled():
            raise HTTPException(status_code=400, detail="GitHub authentication is not configured")
        state = os.urandom(16).hex()
        params = {
            "client_id": self.cfg.github_client_id,
            "redirect_uri": str(request.url_for("github_callback")),
            "scope": "repo read:user",
            "state": state,
        }
        response = RedirectResponse(f"{self.cfg.github_authorize_url}?{urlencode(params)}")
        response.set_cookie(OAUTH_STATE_COOKIE, state, max_age=600, httponly=True, samesite="lax")
        return response

    def callback_response(self, code: str, state: str, request: Request, users: UserStore) -> RedirectResponse:
        if not self.enabled():
            raise HTTPException(status_code=400, detail="GitHub authentication is not configured")
        expected_state = request.cookies.get(OAUTH_STATE_COOKIE)
        if not expected_state or not hmac.compare_digest(expected_state, state):
            raise HTTPException(status_code=400, detail="Invalid GitHub login state")
        access_token = self._exchange_code(code, str(request.url_for("github_callback")))
        username = self._github_username(access_token)
        permission = self.repo_permission(access_token, username)
        role = github_role_for_permission(permission)
        if not role:
            return self._failed_redirect("This GitHub account does not have access to the configured repository.")
        session_id = users.create_oauth_session(username, role, "github", permission, access_token)
        response = RedirectResponse(self.cfg.public_app_url)
        response.delete_cookie(OAUTH_STATE_COOKIE)
        response.set_cookie(COOKIE_NAME, create_token(username, role, "github", session_id), httponly=True, samesite="lax")
        return response

    def repo_permission(self, access_token: str, username: str) -> str:
        owner = self.cfg.github_owner
        repo = self.cfg.github_repo
        if not owner or not repo:
            raise HTTPException(status_code=400, detail="GitHub repository is not configured")
        response = httpx.get(
            f"{self.cfg.github_api_url}/repos/{owner}/{repo}/collaborators/{username}/permission",
            headers=self._headers(access_token),
            timeout=10,
        )
        if response.status_code == 404:
            return "none"
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"GitHub permission check failed ({response.status_code})")
        return response.json().get("permission", "none")

    def refresh_user_permission(self, user: dict, users: UserStore) -> dict:
        if user.get("provider") != "github":
            return user
        session = users.get_oauth_session(user.get("session_id", ""))
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="GitHub session expired")
        permission = self.repo_permission(session["access_token"], user["username"])
        role = github_role_for_permission(permission)
        if not role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="GitHub repository access is required")
        user["role"] = role
        user["permission"] = permission
        return user

    def _exchange_code(self, code: str, redirect_uri: str) -> str:
        response = httpx.post(
            self.cfg.github_token_url,
            headers={"Accept": "application/json"},
            data={
                "client_id": self.cfg.github_client_id,
                "client_secret": self.cfg.github_client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            timeout=10,
        )
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="GitHub token exchange failed")
        token = response.json().get("access_token")
        if not token:
            raise HTTPException(status_code=502, detail="GitHub token response did not include an access token")
        return token

    def _github_username(self, access_token: str) -> str:
        response = httpx.get(f"{self.cfg.github_api_url}/user", headers=self._headers(access_token), timeout=10)
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="GitHub user lookup failed")
        username = response.json().get("login")
        if not username:
            raise HTTPException(status_code=502, detail="GitHub user response did not include a login")
        return username

    def _failed_redirect(self, message: str) -> RedirectResponse:
        return RedirectResponse(f"{self.cfg.public_app_url}?auth_error={quote(message)}")

    @staticmethod
    def _headers(access_token: str) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }


async def current_user(request: Request) -> dict:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    if user.get("provider") == "github":
        session = UserStore().get_oauth_session(user.get("session_id", ""))
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="GitHub session expired")
        return {
            "username": session["username"],
            "role": session["role"],
            "provider": "github",
            "permission": session["permission"],
            "session_id": session["session_id"],
        }
    db_user = UserStore().get_user(user["username"])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return {"username": db_user["username"], "role": db_user["role"], "provider": "local"}


def require_role(user: dict, roles: list[str]) -> None:
    if user["role"] not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
