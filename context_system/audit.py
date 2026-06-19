from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS controlled_context_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    task TEXT NOT NULL,
    record_ids TEXT NOT NULL,
    hashes TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class AuditLog:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA)

    def write(self, run_id: str, task: str, record_ids: list[str], hashes: list[str]) -> None:
        created_at = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO controlled_context_audit
                    (run_id, task, record_ids, hashes, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (run_id, task, json.dumps(record_ids), json.dumps(hashes), created_at),
            )

    def recent(self, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, run_id, task, record_ids, hashes, created_at
                FROM controlled_context_audit
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
