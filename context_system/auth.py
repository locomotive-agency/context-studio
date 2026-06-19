from __future__ import annotations

import base64
import hashlib
import hmac
import os
import sqlite3
import time
from pathlib import Path

from fastapi import HTTPException, Request, Response, status

from .config import get_config

COOKIE_NAME = "context_system_session"
ROLES = ("viewer", "editor", "admin")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'editor', 'admin'))
);
"""


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()
    return password_hash, salt


class UserStore:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or get_config().users_db
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA)
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if count == 0:
                for username, password, role in [
                    ("admin", "admin123", "admin"),
                    ("editor", "editor123", "editor"),
                    ("viewer", "viewer123", "viewer"),
                ]:
                    password_hash, salt = hash_password(password)
                    conn.execute(
                        "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)",
                        (username, password_hash, salt, role),
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


def create_token(username: str, role: str) -> str:
    expiry = int(time.time()) + 86_400
    payload = f"{username}:{role}:{expiry}"
    payload_b64 = base64.urlsafe_b64encode(payload.encode()).decode()
    signature = hmac.new(get_config().secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"


def verify_token(token: str) -> dict | None:
    try:
        payload_b64, signature = token.split(".", 1)
        expected = hmac.new(get_config().secret_key.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        username, role, expiry = base64.urlsafe_b64decode(payload_b64.encode()).decode().split(":")
        if int(expiry) < time.time():
            return None
        return {"username": username, "role": role}
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
    db_user = UserStore().get_user(user["username"])
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return {"username": db_user["username"], "role": db_user["role"]}


def require_role(user: dict, roles: list[str]) -> None:
    if user["role"] not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
