#!/usr/bin/env python3
"""Summarize local tdl export JSON and download directories.

This script never calls Telegram or tdl. It only reads local files.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def human_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def summarize_json(path: Path) -> list[str]:
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - summary tool should report parse failures
        return [f"Export: unreadable JSON ({exc})", f"Output: {path}"]

    lines: list[str] = []
    if isinstance(data, dict) and isinstance(data.get("messages"), list):
        messages = data["messages"]
        media = sum(1 for item in messages if isinstance(item, dict) and item.get("file"))
        text_only = len(messages) - media
        lines.append(f"Export: {len(messages)} messages ({media} with media, {text_only} text-only)")
    elif isinstance(data, dict) and any(k in data for k in ("users", "admins", "bots")):
        users = len(data.get("users") or [])
        admins = len(data.get("admins") or [])
        bots = len(data.get("bots") or [])
        lines.append(f"Export: {users} users, {admins} admins, {bots} bots")
    elif isinstance(data, list):
        lines.append(f"Export: {len(data)} items")
    elif isinstance(data, dict):
        keys = ", ".join(sorted(str(k) for k in data.keys()))
        lines.append(f"Export: unknown JSON object ({keys})")
    else:
        lines.append(f"Export: unknown JSON {type(data).__name__}")

    lines.append(f"Output: {path}")
    return lines


def summarize_dir(path: Path) -> list[str]:
    total = 0
    files = 0
    for root, _, filenames in os.walk(path):
        for name in filenames:
            file_path = Path(root) / name
            try:
                stat = file_path.stat()
            except OSError:
                continue
            if file_path.is_file():
                files += 1
                total += stat.st_size
    return [
        f"Download: {files} files, {human_size(total)}",
        f"Destination: {path}",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize local tdl results")
    parser.add_argument("--export-json", action="append", default=[], help="tdl export JSON path")
    parser.add_argument("--download-dir", action="append", default=[], help="download directory path")
    args = parser.parse_args()

    output: list[str] = []
    for raw in args.export_json:
        path = Path(raw).expanduser()
        if not path.exists():
            output.extend([f"Export: missing JSON", f"Output: {path}"])
        else:
            output.extend(summarize_json(path))

    for raw in args.download_dir:
        path = Path(raw).expanduser()
        if not path.exists():
            output.extend([f"Download: missing directory", f"Destination: {path}"])
        else:
            output.extend(summarize_dir(path))

    if not output:
        parser.error("provide --export-json and/or --download-dir")

    print("\n".join(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
