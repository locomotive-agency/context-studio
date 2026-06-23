from __future__ import annotations

import argparse
import json

import uvicorn

from .config import get_config
from .demo_workspace import initialize_demo_workspace
from .service import ContextService


def main() -> None:
    parser = argparse.ArgumentParser(prog="context-studio")
    subcommands = parser.add_subparsers(dest="command")
    serve = subcommands.add_parser("serve", help="Run the FastAPI and MCP server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8000, type=int)
    subcommands.add_parser("init-demo", help="Create the editable local demo workspace if it does not exist")
    subcommands.add_parser("reset-demo", help="Recreate the editable local demo workspace from tracked demo seeds")
    subcommands.add_parser("stats", help="Print repository statistics")
    subcommands.add_parser("validate", help="Validate the OKF bundle")
    args = parser.parse_args()

    if args.command == "init-demo":
        print(json.dumps(initialize_demo_workspace(get_config(), reset=False), indent=2))
        return
    if args.command == "reset-demo":
        print(json.dumps(initialize_demo_workspace(get_config(), reset=True), indent=2))
        return

    service = ContextService()
    if args.command in (None, "serve"):
        uvicorn.run("context_system.app:app", host=getattr(args, "host", "127.0.0.1"), port=getattr(args, "port", 8000))
        return
    if args.command == "stats":
        print(json.dumps(service.stats(), indent=2))
        return
    report = service.repository.content.validation_report()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["valid"] else 1)
