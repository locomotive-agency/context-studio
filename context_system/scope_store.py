from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .git_store import GitStore
from .models import ScopeNode

SCOPES_FILE = "_scopes.yaml"


class ScopeStore:
    def __init__(self, repository: Path, git: GitStore):
        self.repository = repository
        self.git = git
        self._cache: tuple[int | None, list[dict[str, Any]]] | None = None

    def list_scopes(self) -> list[dict[str, Any]]:
        path = self.repository / SCOPES_FILE
        signature = path.stat().st_mtime_ns if path.exists() else None
        if self._cache and self._cache[0] == signature:
            return [dict(item) for item in self._cache[1]]
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {} if path.exists() else {}
        nodes = [ScopeNode.model_validate(item) for item in data.get("scopes", [])]
        scopes = [node.model_dump() for node in nodes]
        self._cache = (signature, scopes)
        return [dict(item) for item in scopes]

    def save_scope(self, data: dict[str, Any], author: str, existing_id: str | None = None) -> dict[str, Any]:
        scopes = self.list_scopes()
        by_id = {item["id"]: item for item in scopes}
        payload = dict(data)
        if "order" not in payload:
            if existing_id and existing_id in by_id:
                payload["order"] = by_id[existing_id].get("order", 0)
            else:
                parent_id = payload.get("parent_id")
                sibling_orders = [item.get("order", 0) for item in scopes if item.get("parent_id") == parent_id]
                payload["order"] = max(sibling_orders, default=-1) + 1
        node = ScopeNode.model_validate(payload)
        if existing_id and existing_id not in by_id:
            raise ValueError("scope not found")
        if not existing_id and node.id in by_id:
            raise ValueError("scope id already exists")
        if existing_id and node.id != existing_id:
            raise ValueError("scope id cannot be changed")
        if node.parent_id and node.parent_id not in by_id:
            raise ValueError("parent scope not found")
        if node.parent_id == node.id:
            raise ValueError("scope cannot be its own parent")
        ancestor = node.parent_id
        while ancestor:
            if ancestor == node.id:
                raise ValueError("scope hierarchy cannot contain a cycle")
            ancestor = by_id.get(ancestor, {}).get("parent_id")
        if existing_id:
            scopes = [node.model_dump() if item["id"] == existing_id else item for item in scopes]
            action = "Update"
        else:
            scopes.append(node.model_dump())
            action = "Create"
        self._write_scopes(scopes)
        self.git.commit([SCOPES_FILE], f"{action} scope {node.id}", author)
        return node.model_dump()

    def reorder_scopes(self, parent_id: str | None, ordered_ids: list[str], author: str) -> list[dict[str, Any]]:
        scopes = self.list_scopes()
        siblings = [item for item in scopes if item.get("parent_id") == parent_id]
        if len(ordered_ids) != len(set(ordered_ids)) or set(ordered_ids) != {item["id"] for item in siblings}:
            raise ValueError("ordered_ids must contain every sibling scope exactly once")
        order_by_id = {scope_id: index for index, scope_id in enumerate(ordered_ids)}
        updated = [item | {"order": order_by_id[item["id"]]} if item["id"] in order_by_id else item for item in scopes]
        self._write_scopes(updated)
        self.git.commit([SCOPES_FILE], f"Reorder scopes under {parent_id or 'root'}", author)
        return updated

    def move_scope(self, scope_id: str, parent_id: str | None, index: int, author: str) -> list[dict[str, Any]]:
        scopes = self.list_scopes()
        by_id = {item["id"]: item for item in scopes}
        if scope_id not in by_id:
            raise ValueError("scope not found")
        if parent_id and parent_id not in by_id:
            raise ValueError("parent scope not found")
        if parent_id == scope_id:
            raise ValueError("scope cannot be its own parent")
        ancestor = parent_id
        while ancestor:
            if ancestor == scope_id:
                raise ValueError("scope cannot be moved under one of its descendants")
            ancestor = by_id[ancestor].get("parent_id")

        source = by_id[scope_id]
        old_parent_id = source.get("parent_id")
        new_siblings = sorted(
            [item for item in scopes if item.get("parent_id") == parent_id and item["id"] != scope_id],
            key=lambda item: (item.get("order", 0), item["name"]),
        )
        target_index = max(0, min(index, len(new_siblings)))
        moved = source | {"parent_id": parent_id}
        new_siblings.insert(target_index, moved)
        updates = {item["id"]: item | {"order": order} for order, item in enumerate(new_siblings)}

        if old_parent_id != parent_id:
            old_siblings = sorted(
                [item for item in scopes if item.get("parent_id") == old_parent_id and item["id"] != scope_id],
                key=lambda item: (item.get("order", 0), item["name"]),
            )
            updates.update({item["id"]: item | {"order": order} for order, item in enumerate(old_siblings)})

        updated = [updates.get(item["id"], item) for item in scopes]
        self._write_scopes(updated)
        destination = parent_id or "root"
        self.git.commit([SCOPES_FILE], f"Move scope {scope_id} under {destination}", author)
        return updated

    def delete_scope(self, scope_id: str, author: str, assigned_scope_ids: set[str]) -> None:
        scopes = self.list_scopes()
        if not any(item["id"] == scope_id for item in scopes):
            raise ValueError("scope not found")
        if any(item.get("parent_id") == scope_id for item in scopes):
            raise ValueError("scope has child scopes")
        if scope_id in assigned_scope_ids:
            raise ValueError("scope is assigned to documents")
        self._write_scopes([item for item in scopes if item["id"] != scope_id])
        self.git.commit([SCOPES_FILE], f"Delete scope {scope_id}", author)

    def scope_ancestors(self, scope_id: str) -> list[str]:
        by_id = {item["id"]: item for item in self.list_scopes()}
        if scope_id not in by_id:
            raise ValueError("scope not found")
        chain = []
        current: str | None = scope_id
        while current:
            chain.append(current)
            current = by_id[current].get("parent_id")
        return list(reversed(chain))

    def _write_scopes(self, scopes: list[dict[str, Any]]) -> None:
        path = self.repository / SCOPES_FILE
        path.write_text(yaml.safe_dump({"scopes": scopes}, sort_keys=False), encoding="utf-8")
        self._cache = (path.stat().st_mtime_ns, [dict(item) for item in scopes])
