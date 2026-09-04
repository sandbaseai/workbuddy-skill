#!/usr/bin/env python3
"""Deterministic provenance-context signals for catalog records."""

from __future__ import annotations

import re

DORMANT_TERMS = {"archive", "archived", "backup", "backups", "deprecated", "disabled", "legacy", "obsolete"}
COPY_TERMS = {"fork", "forks", "mirror", "mirrors"}


def source_signals(row: dict) -> list[str]:
    signals = []
    if row.get("repository_fork"):
        signals.append("repository-fork")
    repository = str(row.get("repository", "")).casefold()
    path = str(row.get("path", "")).casefold()
    repository_tokens = set(re.findall(r"[a-z0-9]+", repository))
    path_parts = {part.strip("._-") for part in path.split("/")}
    if repository_tokens & {"mirror", "mirrors"} or path_parts & COPY_TERMS:
        signals.append("copy-or-mirror-path")
    if path_parts & DORMANT_TERMS or any(
        part.endswith(tuple(f".{term}" for term in DORMANT_TERMS)) for part in path_parts
    ):
        signals.append("dormant-path")
    return signals


def source_context(row: dict) -> str:
    return "review-source" if source_signals(row) else "primary-looking"
