from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_DIR / "config.json"


class Config(BaseModel):
    domain: str = "pipeline.zoominfo.com"
    internal_domains: list[str] = Field(default_factory=lambda: ["pipeline.zoominfo.com", "zoominfo.com"])
    context_server_name: str = "marketing-context"
    context_repository_path: str = "context_repo"
    audit_path: str = "var/audit.sqlite"
    users_path: str = "var/users.sqlite"
    connectors: list[str] = Field(default_factory=lambda: ["local"])
    default_remote_url: str = "http://localhost:8000"
    secret_key: str = "change-me-in-production"
    embedding_model: Optional[str] = None

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
