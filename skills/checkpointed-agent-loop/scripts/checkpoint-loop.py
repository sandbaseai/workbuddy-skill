#!/usr/bin/env python3
"""Small, dependency-free durable checkpoint state machine for WorkBuddy."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STATES = {"planned", "running", "verifying", "succeeded", "failed", "blocked"}
TERMINAL = {"succeeded", "failed", "blocked"}
TRANSITIONS = {
    "planned": {"running"},
    "running": {"verifying", "failed", "blocked"},
    "verifying": {"succeeded", "running", "failed", "blocked"},
    "succeeded": set(),
    "failed": set(),
    "blocked": set(),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"checkpoint not found: {path}")
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid checkpoint: {exc}")
    if not isinstance(data, dict) or data.get("state") not in STATES:
        fail("malformed checkpoint state")
    required = {"task", "objective", "max_attempts", "attempts", "next_action", "history", "evidence"}
    if not required.issubset(data):
        fail("checkpoint is missing required fields")
    if not isinstance(data["max_attempts"], int) or data["max_attempts"] < 1:
        fail("max_attempts must be a positive integer")
    if not isinstance(data["attempts"], int) or not 0 <= data["attempts"] <= data["max_attempts"]:
        fail("attempt count is outside its budget")
    if not isinstance(data["history"], list) or not isinstance(data["evidence"], list):
        fail("history and evidence must be lists")
    return data


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except OSError as exc:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        fail(f"could not persist checkpoint: {exc}")


def add_history(data: dict, event: str, **extra: str) -> None:
    data["history"].append({"at": now(), "event": event, **extra})


def cmd_init(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if path.exists():
        fail(f"refusing to overwrite checkpoint: {path}")
    data = {
        "schema": "workbuddy.checkpoint/v1",
        "task": args.task,
        "objective": args.objective,
        "state": "planned",
        "max_attempts": args.max_attempts,
        "attempts": 0,
        "next_action": args.next_action,
        "created_at": now(),
        "updated_at": now(),
        "history": [],
        "evidence": [],
    }
    save(path, data)
    print(f"initialized {path}")


def cmd_status(args: argparse.Namespace) -> None:
    data = load(Path(args.file))
    if args.format == "summary":
        print(f"{data['task']}: {data['state']} ({data['attempts']}/{data['max_attempts']} attempts)")
        print(f"next: {data['next_action']}")
        print(f"evidence: {len(data['evidence'])}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_transition(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = load(path)
    old, new = data["state"], args.to
    if new not in TRANSITIONS[old]:
        fail(f"illegal transition: {old} -> {new}")
    if old in TERMINAL:
        fail("terminal checkpoint is immutable")
    if new == "running":
        if data["attempts"] >= data["max_attempts"]:
            fail("attempt budget exhausted")
        if not args.next_action and not data["next_action"]:
            fail("running requires next_action")
        data["attempts"] += 1
        if args.next_action:
            data["next_action"] = args.next_action
    if new in {"failed", "blocked", "running"} and args.reason:
        data["reason"] = args.reason
    if new == "succeeded" and not any(e.get("outcome") == "passed" for e in data["evidence"]):
        fail("succeeded requires passing evidence")
    data["state"] = new
    data["updated_at"] = now()
    add_history(data, f"{old}->{new}", reason=args.reason or "")
    save(path, data)
    print(f"{old} -> {new}")


def cmd_evidence(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = load(path)
    if data["state"] != "verifying":
        fail("evidence can only be recorded in verifying state")
    if args.outcome not in {"passed", "failed"}:
        fail("outcome must be passed or failed")
    artifact = Path(args.artifact) if args.artifact else None
    if artifact and not artifact.exists():
        fail(f"artifact does not exist: {artifact}")
    record = {"at": now(), "check": args.check, "outcome": args.outcome}
    if artifact:
        record["artifact"] = str(artifact)
    data["evidence"].append(record)
    data["updated_at"] = now()
    add_history(data, f"evidence:{args.outcome}", check=args.check)
    save(path, data)
    print(f"recorded {args.outcome} evidence")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--file", required=True); init.add_argument("--task", required=True)
    init.add_argument("--objective", required=True); init.add_argument("--max-attempts", type=int, required=True)
    init.add_argument("--next-action", required=True); init.set_defaults(func=cmd_init)
    status = sub.add_parser("status"); status.add_argument("--file", required=True)
    status.add_argument("--format", choices=["summary", "json"], default="json"); status.set_defaults(func=cmd_status)
    trans = sub.add_parser("transition"); trans.add_argument("--file", required=True)
    trans.add_argument("--to", choices=sorted(STATES), required=True); trans.add_argument("--next-action")
    trans.add_argument("--reason"); trans.set_defaults(func=cmd_transition)
    evidence = sub.add_parser("evidence"); evidence.add_argument("--file", required=True)
    evidence.add_argument("--check", required=True); evidence.add_argument("--outcome", required=True)
    evidence.add_argument("--artifact"); evidence.set_defaults(func=cmd_evidence)
    return p


if __name__ == "__main__":
    parsed = parser().parse_args()
    parsed.func(parsed)
