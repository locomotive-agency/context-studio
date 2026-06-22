from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
import time
from pathlib import Path, PurePosixPath

from .config import Config, get_config

TOKEN_RE = re.compile(r"[a-z0-9]+")
VECTOR_SIZE = 64

SCHEMA = """
CREATE TABLE IF NOT EXISTS collections (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_documents (
    id TEXT PRIMARY KEY,
    collection_id TEXT NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    source_title TEXT NOT NULL,
    source_path TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT '',
    content_hash TEXT NOT NULL,
    modified_time INTEGER NOT NULL,
    index_status TEXT NOT NULL,
    error TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS collection_units (
    id TEXT PRIMARY KEY,
    collection_id TEXT NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    document_id TEXT NOT NULL REFERENCES collection_documents(id) ON DELETE CASCADE,
    source_path TEXT NOT NULL,
    location TEXT NOT NULL,
    text TEXT NOT NULL,
    content_hash TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS collection_units_fts USING fts5(
    unit_id UNINDEXED,
    text
);

CREATE TABLE IF NOT EXISTS collection_unit_embeddings (
    unit_id TEXT PRIMARY KEY REFERENCES collection_units(id) ON DELETE CASCADE,
    embedding_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id TEXT NOT NULL,
    document_id TEXT,
    message TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
"""


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9._-]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("collection id cannot be blank")
    return slug


class CollectionManager:
    def __init__(self, config: Config | None = None):
        self.config = config or get_config()
        self.root = self.config.collections_root
        self.db_path = self.config.collections_db
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def create_collection(self, collection_id: str, name: str | None = None, description: str = "") -> dict:
        clean_id = slugify(collection_id)
        display_name = name or collection_id
        now = int(time.time())
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO collections (id, name, description, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET name = excluded.name, description = excluded.description
                """,
                (clean_id, display_name, description, now),
            )
        (self.root / clean_id / "sources").mkdir(parents=True, exist_ok=True)
        return self.get_collection(clean_id)

    def list_collections(self) -> list[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT id, name, description, created_at FROM collections ORDER BY name").fetchall()
        return [dict(row) for row in rows]

    def get_collection(self, collection_id: str) -> dict:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT id, name, description, created_at FROM collections WHERE id = ?",
                (slugify(collection_id),),
            ).fetchone()
        if not row:
            raise ValueError("collection not found")
        return dict(row)

    def list_documents(self, collection_id: str) -> list[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, collection_id, source_title, source_path, mime_type, content_hash, modified_time, index_status, error
                FROM collection_documents
                WHERE collection_id = ?
                ORDER BY source_title
                """,
                (slugify(collection_id),),
            ).fetchall()
        return [self._with_logical_source_path(dict(row)) for row in rows]

    def add_document_text(self, collection_id: str, filename: str, text: str) -> dict:
        return self.add_document_bytes(collection_id, filename, text.encode("utf-8"))

    def add_document_bytes(self, collection_id: str, filename: str, content: bytes) -> dict:
        clean_id = slugify(collection_id)
        self.get_collection(clean_id)
        safe_name = PurePosixPath(filename).name
        if not safe_name:
            raise ValueError("filename is required")
        sources_dir = self.root / clean_id / "sources"
        sources_dir.mkdir(parents=True, exist_ok=True)
        stored_path = sources_dir / safe_name
        stored_path.write_bytes(content)
        content_hash = hashlib.sha256(content).hexdigest()
        document_id = hashlib.sha256(f"{clean_id}:{safe_name}:{content_hash}".encode()).hexdigest()[:16]
        now = int(time.time())
        try:
            text = self._parse_source(stored_path)
            units = self._split_units(text)
            index_status = "indexed"
            error = ""
        except Exception as exc:
            units = []
            index_status = "error"
            error = str(exc)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO collection_documents
                (id, collection_id, source_title, source_path, mime_type, content_hash, modified_time, index_status, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (document_id, clean_id, safe_name, str(stored_path), stored_path.suffix.lower(), content_hash, now, index_status, error),
            )
            existing = [row[0] for row in conn.execute("SELECT id FROM collection_units WHERE document_id = ?", (document_id,)).fetchall()]
            for unit_id in existing:
                conn.execute("DELETE FROM collection_units_fts WHERE unit_id = ?", (unit_id,))
                conn.execute("DELETE FROM collection_unit_embeddings WHERE unit_id = ?", (unit_id,))
            conn.execute("DELETE FROM collection_units WHERE document_id = ?", (document_id,))
            for index, unit_text in enumerate(units, start=1):
                unit_hash = hashlib.sha256(unit_text.encode("utf-8")).hexdigest()
                unit_id = f"{document_id}#p{index}"
                location = f"paragraph {index}"
                conn.execute(
                    """
                    INSERT INTO collection_units
                    (id, collection_id, document_id, source_path, location, text, content_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (unit_id, clean_id, document_id, str(stored_path), location, unit_text, unit_hash),
                )
                conn.execute("INSERT INTO collection_units_fts (unit_id, text) VALUES (?, ?)", (unit_id, unit_text))
                conn.execute(
                    "INSERT INTO collection_unit_embeddings (unit_id, embedding_json) VALUES (?, ?)",
                    (unit_id, json.dumps(self._embedding(unit_text))),
                )
            if error:
                conn.execute(
                    "INSERT INTO collection_errors (collection_id, document_id, message, created_at) VALUES (?, ?, ?, ?)",
                    (clean_id, document_id, error, now),
                )
        return self._document(document_id)

    def search(self, collection_ids: list[str], query: str, top_k: int = 5) -> list[dict]:
        clean_ids = [slugify(collection_id) for collection_id in collection_ids]
        if not clean_ids or not query.strip() or top_k <= 0:
            return []
        known = {collection["id"] for collection in self.list_collections()}
        clean_ids = [collection_id for collection_id in clean_ids if collection_id in known]
        if not clean_ids:
            return []
        bm25_scores = self._bm25_scores(clean_ids, query)
        vector_scores = self._vector_scores(clean_ids, query)
        unit_ids = set(bm25_scores) | set(vector_scores)
        scored = [(unit_id, bm25_scores.get(unit_id, 0.0) + vector_scores.get(unit_id, 0.0)) for unit_id in unit_ids]
        scored = sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
        if not scored:
            return []
        details = self._units([unit_id for unit_id, _score in scored])
        by_id = {unit["id"]: unit for unit in details}
        results = []
        for unit_id, score in scored:
            unit = by_id.get(unit_id)
            if not unit:
                continue
            results.append(
                {
                    "text": unit["text"],
                    "score": round(score, 6),
                    "citation": {
                        "collection_id": unit["collection_id"],
                        "source_document_id": unit["document_id"],
                        "source_title": unit["source_title"],
                        "source_path": self._logical_source_path(unit["source_path"], unit["collection_id"]),
                        "location": unit["location"],
                        "unit_id": unit["id"],
                        "content_hash": unit["content_hash"],
                    },
                }
            )
        return results

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _document(self, document_id: str) -> dict:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                """
                SELECT id, collection_id, source_title, source_path, mime_type, content_hash, modified_time, index_status, error
                FROM collection_documents
                WHERE id = ?
                """,
                (document_id,),
            ).fetchone()
        if not row:
            raise ValueError("document not found")
        return self._with_logical_source_path(dict(row))

    def _units(self, unit_ids: list[str]) -> list[dict]:
        placeholders = ",".join("?" for _ in unit_ids)
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                f"""
                SELECT u.id, u.collection_id, u.document_id, u.source_path, u.location, u.text, u.content_hash, d.source_title
                FROM collection_units u
                JOIN collection_documents d ON d.id = u.document_id
                WHERE u.id IN ({placeholders})
                """,
                unit_ids,
            ).fetchall()
        return [dict(row) for row in rows]

    def _with_logical_source_path(self, row: dict) -> dict:
        if "source_path" in row and "collection_id" in row:
            row = dict(row)
            row["source_path"] = self._logical_source_path(row["source_path"], row["collection_id"])
        return row

    def _logical_source_path(self, source_path: str, collection_id: str) -> str:
        path = Path(source_path)
        clean_id = slugify(collection_id)
        try:
            relative = path.resolve().relative_to((self.root / clean_id).resolve())
            return PurePosixPath(clean_id, relative.as_posix()).as_posix()
        except (OSError, ValueError):
            return PurePosixPath(clean_id, "sources", path.name).as_posix()

    def _bm25_scores(self, collection_ids: list[str], query: str) -> dict[str, float]:
        terms = tokenize(query)
        if not terms:
            return {}
        match_query = " OR ".join(terms)
        placeholders = ",".join("?" for _ in collection_ids)
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT f.unit_id, bm25(collection_units_fts) AS rank
                FROM collection_units_fts f
                JOIN collection_units u ON u.id = f.unit_id
                WHERE collection_units_fts MATCH ?
                  AND u.collection_id IN ({placeholders})
                ORDER BY rank
                LIMIT 50
                """,
                [match_query, *collection_ids],
            ).fetchall()
        return {unit_id: 1 / (1 + max(rank, 0)) for unit_id, rank in rows}

    def _vector_scores(self, collection_ids: list[str], query: str) -> dict[str, float]:
        query_vector = self._embedding(query)
        placeholders = ",".join("?" for _ in collection_ids)
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT u.id, e.embedding_json
                FROM collection_units u
                JOIN collection_unit_embeddings e ON e.unit_id = u.id
                WHERE u.collection_id IN ({placeholders})
                """,
                collection_ids,
            ).fetchall()
        scores = {}
        for unit_id, embedding_json in rows:
            score = self._cosine(query_vector, json.loads(embedding_json))
            if score > 0:
                scores[unit_id] = score
        return scores

    def _parse_source(self, path: Path) -> str:
        try:
            from markitdown import MarkItDown
        except ImportError:
            if path.suffix.lower() in {".md", ".txt", ".csv", ".json"}:
                return path.read_text(encoding="utf-8", errors="replace")
            raise RuntimeError("MarkItDown is required to parse this file type")
        result = MarkItDown().convert(str(path))
        text = getattr(result, "text_content", "") or str(result)
        return text

    @staticmethod
    def _split_units(text: str) -> list[str]:
        units = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
        if not units and text.strip():
            units = [text.strip()]
        return units

    @staticmethod
    def _embedding(text: str) -> list[float]:
        vector = [0.0] * VECTOR_SIZE
        for token in tokenize(text):
            index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % VECTOR_SIZE
            vector[index] += 1.0
        length = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / length for value in vector]

    @staticmethod
    def _cosine(left: list[float], right: list[float]) -> float:
        return sum(a * b for a, b in zip(left, right))
