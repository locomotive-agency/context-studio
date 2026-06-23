from __future__ import annotations

import shutil
from pathlib import Path

from .collections import CollectionManager
from .config import Config, PROJECT_DIR
from .git_store import GitStore

DEMO_CONTEXT_REPO = PROJECT_DIR / "demo" / "context_repo"
DEMO_SALES_CONVERSATIONS = PROJECT_DIR / "demo" / "sample_sources" / "sales-conversations"
DEMO_COLLECTION_ID = "enterprise-sales-conversations"


def initialize_demo_workspace(config: Config, *, reset: bool = False) -> dict:
    """Create an editable local workspace from tracked demo seed files."""
    cleared_databases = _clear_runtime_databases(config) if reset else []
    copied_context = _copy_context_repo(config.context_repo, reset=reset)
    baseline_commit = _ensure_context_repo_baseline(config.context_repo, copied=copied_context)
    collection = _seed_collection(config, reset=reset)
    return {
        "context_repository_path": str(config.context_repo),
        "collections_db_path": str(config.collections_db),
        "collections_root_path": str(config.collections_root),
        "copied_context_repo": copied_context,
        "baseline_commit": baseline_commit,
        "cleared_databases": cleared_databases,
        "collection": collection,
    }


def _copy_context_repo(target: Path, *, reset: bool) -> bool:
    if not DEMO_CONTEXT_REPO.is_dir():
        raise FileNotFoundError(f"demo context repository not found: {DEMO_CONTEXT_REPO}")
    if target.exists():
        if not reset:
            return False
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DEMO_CONTEXT_REPO, target)
    return True


def _clear_runtime_databases(config: Config) -> list[str]:
    cleared = []
    for path in [config.audit_db, config.users_db]:
        if path.exists():
            path.unlink()
            cleared.append(str(path))
    return cleared


def _ensure_context_repo_baseline(target: Path, *, copied: bool) -> str:
    git = GitStore(target)
    if not copied and git.head() != "uncommitted":
        return git.head()
    paths = [
        path.relative_to(target).as_posix()
        for path in sorted(target.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    ]
    return git.commit(paths, "Initialize demo context repository", "system")


def _seed_collection(config: Config, *, reset: bool) -> dict:
    if not DEMO_SALES_CONVERSATIONS.is_dir():
        raise FileNotFoundError(f"demo sales conversations not found: {DEMO_SALES_CONVERSATIONS}")
    if reset:
        if config.collections_db.exists():
            config.collections_db.unlink()
        if config.collections_root.exists():
            shutil.rmtree(config.collections_root)

    manager = CollectionManager(config)
    collection = manager.create_collection(
        DEMO_COLLECTION_ID,
        "Enterprise Sales Conversations",
        "Synthetic sales conversations for testing cited Collection retrieval.",
    )
    indexed = 0
    for path in sorted(DEMO_SALES_CONVERSATIONS.glob("*.md")):
        if path.name == "README.md":
            continue
        manager.add_document_text(collection["id"], path.name, path.read_text(encoding="utf-8"))
        indexed += 1
    collection["indexed_sources"] = indexed
    return collection
