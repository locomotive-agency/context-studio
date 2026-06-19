from __future__ import annotations

import subprocess
from pathlib import Path


class GitStore:
    def __init__(self, repository: Path):
        self.content_root = repository.resolve()
        self.content_root.mkdir(parents=True, exist_ok=True)
        discovered = subprocess.run(["git", "-C", str(self.content_root), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if discovered.returncode == 0:
            self.repository = Path(discovered.stdout.strip())
        else:
            self.repository = self.content_root
            self._run("init", "--initial-branch=main")
            self._run("config", "user.name", "Context System")
            self._run("config", "user.email", "context-system@localhost")
        relative = self.content_root.relative_to(self.repository)
        self.path_prefix = "" if relative == Path(".") else relative.as_posix()

    def commit(self, paths: list[str], message: str, author: str) -> str:
        git_paths = [self._content_path(path) for path in paths]
        self._run("add", "--", *git_paths)
        staged = self._run("diff", "--cached", "--quiet", check=False)
        if staged.returncode == 0:
            return self.head()
        author_value = f"{author} <{author}@context.local>"
        self._run("commit", "-m", message, f"--author={author_value}")
        return self.head()

    def history(self, path: str | None = None, limit: int = 30) -> list[dict[str, str]]:
        args = ["log", f"-{limit}", "--format=%H%x1f%h%x1f%an%x1f%aI%x1f%s"]
        if path:
            args.extend(["--", self._content_path(path)])
        result = self._run(*args, check=False)
        if result.returncode != 0:
            return []
        history = []
        for line in result.stdout.splitlines():
            full_hash, short_hash, author, timestamp, subject = line.split("\x1f", 4)
            history.append({"hash": full_hash, "short_hash": short_hash, "author": author, "timestamp": timestamp, "subject": subject})
        return history

    def diff(self, commit: str, path: str | None = None) -> str:
        args = ["show", "--format=", "--no-ext-diff", commit]
        if path:
            args.extend(["--", self._content_path(path)])
        return self._run(*args).stdout

    def status(self) -> list[str]:
        args = ["status", "--short"]
        if self.path_prefix:
            args.extend(["--", self.path_prefix])
        return self._run(*args).stdout.splitlines()

    def head(self) -> str:
        result = self._run("rev-parse", "--short", "HEAD", check=False)
        return result.stdout.strip() if result.returncode == 0 else "uncommitted"

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repository), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def _content_path(self, path: str) -> str:
        return f"{self.path_prefix}/{path}" if self.path_prefix else path
