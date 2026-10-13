#!/usr/bin/env python3
"""Offline consistency checks, not a substitute for host/runtime validation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def inside(root: Path, raw: str) -> Path:
    if not raw.startswith("./") or ".." in Path(raw).parts:
        raise ValueError(f"unsafe package path: {raw}")
    path = (root / raw).resolve()
    if not path.is_relative_to(root.resolve()) or not path.exists():
        raise ValueError(f"missing/escaping package path: {raw}")
    return path


def validate(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    skill = root / "skills/scrum-skill/SKILL.md"
    body = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", body, re.S)
    if not match:
        raise ValueError("skill frontmatter is missing")
    fields = dict(line.split(": ", 1) for line in match[1].splitlines())
    if fields.get("name") != "scrum-skill" or not fields.get("description"):
        raise ValueError("skill identity/description is missing")
    version = json.loads((root / "skills/scrum-skill/assets/version.json").read_text())["version"]
    for relative in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        manifest = json.loads((root / relative).read_text(encoding="utf-8"))
        if (manifest.get("name"), manifest.get("version")) != (fields["name"], version):
            raise ValueError(f"manifest identity/version drift: {relative}")
        if not manifest.get("description"):
            raise ValueError(f"missing manifest description: {relative}")
        if "skills" in manifest and inside(root, manifest["skills"]) != skill.parent.parent:
            raise ValueError("manifest must reference the canonical skill directory")
    codex = json.loads((root / ".agents/plugins/marketplace.json").read_text())
    claude = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    if codex.get("name") != claude.get("name") or not claude.get("owner", {}).get("name"):
        raise ValueError("marketplace identity/owner mismatch")
    for catalog in (codex, claude):
        if len(catalog.get("plugins", [])) != 1:
            raise ValueError("expected one canonical plugin")
        entry = catalog["plugins"][0]
        if entry.get("name") != fields["name"]:
            raise ValueError("plugin entry identity mismatch")
        source = entry["source"]
        path = source["path"] if isinstance(source, dict) else source
        if inside(root, path) != root:
            raise ValueError("catalog must reference repository-root plugin")
    policy = codex["plugins"][0].get("policy", {})
    if not policy.get("installation") or not policy.get("authentication"):
        raise ValueError("Codex catalog policy metadata missing")
    for file in root.rglob("*.md"):
        if any(part.startswith(".") for part in file.relative_to(root).parts):
            continue
        text = file.read_text(encoding="utf-8")
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"[a-z]+://", target):
                continue
            path = (file.parent / target).resolve()
            if not path.is_relative_to(root) or not path.exists():
                raise ValueError(f"broken local reference in {file.relative_to(root)}: {target}")
    # Publication boundary: local state/source documents never belong in this package.
    for file in root.rglob("*"):
        relative = file.relative_to(root)
        if any(p in {".git", ".eval-output", "__pycache__", "node_modules"} for p in relative.parts):
            continue
        if file.is_file() and (file.suffix.lower() == ".pdf" or relative.parts[0] in {"private", ".scrum"}):
            raise ValueError(f"local/source document in distributable tree: {relative}")
    return ["canonical skill/manifests/catalogs agree", "local references resolve",
            "no project-private records or source PDFs in distributable tree"]


if __name__ == "__main__":
    try:
        for result in validate():
            print(f"PASS: {result}")
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
