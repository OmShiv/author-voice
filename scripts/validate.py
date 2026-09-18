#!/usr/bin/env python3
"""Validate this package's manifests, references, eval inputs and generated files."""

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate():
    plugin = ROOT / "plugins/author-voice"
    skill = plugin / "skills/author-voice"
    manifests = [json.loads((plugin / path).read_text(encoding="utf-8")) for path in ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json")]
    if any(m["name"] != "author-voice" or m["version"] != manifests[0]["version"] for m in manifests):
        raise ValueError("Plugin identities/versions differ")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifests[0]["version"]):
        raise ValueError("Use a semantic release version")
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\nname: author-voice\ndescription: ") or "\n---\n" not in text[4:]:
        raise ValueError("Invalid canonical skill frontmatter")
    for path in skill.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in target and not (path.parent / target).is_file():
                raise ValueError(f"Missing resource from {path}: {target}")
    cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
    seen = set()
    for case in cases:
        if not re.fullmatch(r"[a-z0-9-]+", case["id"]) or case["id"] in seen:
            raise ValueError("Invalid/duplicate eval case id")
        seen.add(case["id"])
        if not case["review"] or any(lock not in case["source"] for lock in case["locks"]):
            raise ValueError(f"Invalid eval criteria/locks: {case['id']}")
    market = json.loads((ROOT / "packaging/openai-marketplace.json").read_text(encoding="utf-8"))
    entry = market["plugins"][0]
    if entry["source"]["path"] != "./plugins/author-voice" or entry["name"] != "author-voice":
        raise ValueError("Marketplace does not resolve to the packaged plugin")
    public_market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    if public_market["name"] != "author-voice" or public_market["plugins"][0]["source"] != "./plugins/author-voice":
        raise ValueError("Public Claude marketplace does not resolve to the plugin")
    for field in ("logo", "composerIcon"):
        if not (plugin / manifests[2]["interface"][field]).is_file():
            raise ValueError(f"Missing {field} asset")
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], check=True)
    print(f"Validated three manifests, skill references, and {len(cases)} evaluation cases.")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"validate: {error}", file=sys.stderr)
        raise SystemExit(1)
