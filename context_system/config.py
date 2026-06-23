from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, Field

PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_DIR / "config.json"


class LocalDemoUser(BaseModel):
    username: str
    password: str
    role: Literal["viewer", "editor", "admin"]


class Config(BaseModel):
    domain: str = "contextstudio.example.com"
    internal_domains: list[str] = Field(default_factory=lambda: ["contextstudio.example.com"])
    context_server_name: str = "context-studio"
    context_repository_path: str = ".local/context_repo"
    audit_path: str = ".local/var/audit.sqlite"
    users_path: str = ".local/var/users.sqlite"
    collections_root_path: str = ".local/var/collections"
    collections_db_path: str = ".local/var/collections.sqlite"
    connectors: list[str] = Field(default_factory=lambda: ["local"])
    mcp_servers: list[str | dict] = Field(default_factory=list)
    mcp_service_account_role: Optional[Literal["viewer", "editor", "admin"]] = None
    default_remote_url: str = "http://localhost:8000"
    secret_key: str = "change-me-in-production"
    local_demo_users: list[LocalDemoUser] = Field(default_factory=list)
    embedding_model: Optional[str] = None
    vector_store: str = "sqlite"
    public_app_url: str = "http://127.0.0.1:4321"
    github_owner: Optional[str] = None
    github_repo: Optional[str] = None
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    github_api_url: str = "https://api.github.com"
    github_authorize_url: str = "https://github.com/login/oauth/authorize"
    github_token_url: str = "https://github.com/login/oauth/access_token"

    _base: Path = PROJECT_DIR

    def path(self, value: str | Path) -> Path:
        path = Path(value)
        return path if path.is_absolute() else (self._base / path).resolve()

    @property
    def kb_path(self) -> Path:
        return self.context_repo

    @property
    def context_repo(self) -> Path:
        return self.path(self.context_repository_path)

    @property
    def audit_db(self) -> Path:
        return self.path(self.audit_path)

    @property
    def users_db(self) -> Path:
        return self.path(self.users_path)

    @property
    def collections_root(self) -> Path:
        return self.path(self.collections_root_path)

    @property
    def collections_db(self) -> Path:
        return self.path(self.collections_db_path)

    @property
    def github_enabled(self) -> bool:
        return all([self.github_owner, self.github_repo, self.github_client_id, self.github_client_secret])

    @property
    def github_full_name(self) -> str | None:
        if not self.github_owner or not self.github_repo:
            return None
        return f"{self.github_owner}/{self.github_repo}"

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "Config":
        path = Path(config_path) if config_path else DEFAULT_CONFIG
        data = {}
        if path.exists():
            data = {k: v for k, v in json.loads(path.read_text()).items() if not k.startswith("_")}
        for field in cls.model_fields:
            env = os.environ.get(f"CS_{field.upper()}")
            if env is None:
                continue
            try:
                data[field] = json.loads(env)
            except json.JSONDecodeError:
                data[field] = env
        cfg = cls(**data)
        cfg._base = path.resolve().parent
        return cfg


_CONFIG: Config | None = None


def get_config() -> Config:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = Config.load()
    return _CONFIG
