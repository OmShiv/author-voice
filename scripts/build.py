#!/usr/bin/env python3
"""Build portable instructions and reproducible archives from one skill source."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/author-voice"
SKILL = PLUGIN / "skills/author-voice"
OUTPUT_PATHS = ["platforms/chatgpt/instructions.md", "platforms/gemini/instructions.md", "platforms/shared/knowledge.md"]
ARCHIVE_NAMES = [f"author-voice-{kind}.zip" for kind in ("skill", "plugin", "openai-marketplace", "chatgpt", "gemini")]


def generated() -> dict[str, str]:
    source = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    body = source.split("---", 2)[2].strip().split("## Conditional resources", 1)[0].strip()
    portable = body + "\n\n## Optional knowledge\n\nIf author-voice-knowledge.md is attached, consult only its relevant sections for papers, books, profiles, and artifacts. The core instructions here are sufficient when it is absent. Use only tools actually available in this conversation; never claim that a document was edited, exported, or visually checked without doing it.\n"
    knowledge = "# Author Voice supporting knowledge\n\nOptional reference material. Apply the configured core instructions first. File and script operations described here require corresponding tools; attachment as knowledge does not install a script or connector.\n\n"
    for name in ("paper", "book", "voice-profile", "artifacts", "examples"):
        knowledge += (SKILL / f"references/{name}.md").read_text(encoding="utf-8") + "\n\n"
    return {
        OUTPUT_PATHS[0]: portable,
        OUTPUT_PATHS[1]: portable,
        OUTPUT_PATHS[2]: knowledge.rstrip() + "\n",
    }


def source_files(directory: Path):
    return sorted(p for p in directory.rglob("*") if p.is_file() and not p.is_symlink() and "__pycache__" not in p.parts and p.name != ".DS_Store" and p.suffix != ".pyc")


def archive(path: Path, entries: dict[str, bytes]):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            out.writestr(info, content)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated tracked files without writing.")
    args = parser.parse_args(argv)
    outputs = generated()
    # A conservative packaging budget, not a claim about every platform's limit.
    for name in OUTPUT_PATHS[:2]:
        if len(outputs[name]) > 8000:
            raise ValueError(f"{name} exceeds the project's 8,000-character instruction budget")
    if args.check:
        stale = [p for p, text in outputs.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding="utf-8") != text]
        if stale:
            print("Regenerate with python3 scripts/build.py: " + ", ".join(stale), file=sys.stderr)
            return 1
        print("Generated instructions match the canonical skill.")
        return 0
    for name, text in outputs.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    notices = {name: (ROOT / source).read_bytes() for name, source in (("LICENSE", "LICENSE"), ("PRIVACY.md", "docs/privacy.md"), ("TERMS.md", "docs/terms.md")) if (ROOT / source).is_file()}
    archive(dist / "author-voice-skill.zip", {**{"author-voice/" + str(p.relative_to(SKILL)): p.read_bytes() for p in source_files(SKILL)}, **{"author-voice/" + name: data for name, data in notices.items()}})
    archive(dist / "author-voice-plugin.zip", {**{str(p.relative_to(PLUGIN)): p.read_bytes() for p in source_files(PLUGIN)}, **notices})
    bundle = {"instructions.md": outputs[OUTPUT_PATHS[0]].encode(), "author-voice-knowledge.md": outputs[OUTPUT_PATHS[2]].encode(), "starter-profile.md": (ROOT / "profiles/starter.md").read_bytes(), **notices}
    for platform in ("chatgpt", "gemini"):
        archive(dist / f"author-voice-{platform}.zip", {**bundle, "SETUP.md": (ROOT / f"platforms/{platform}/SETUP.md").read_bytes()})
    # A complete, relocatable marketplace; no writes to user configuration.
    market = dist / "openai-marketplace"
    target = market / "plugins/author-voice"
    # Replace this generated subtree so removed source files cannot survive a build.
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(PLUGIN, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
    for name, data in notices.items():
        (target / name).write_bytes(data)
    metadata = market / ".agents/plugins/marketplace.json"
    metadata.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "packaging/openai-marketplace.json", metadata)
    archive(dist / "author-voice-openai-marketplace.zip", {str(p.relative_to(market)): p.read_bytes() for p in source_files(market)})
    checksums = {name: hashlib.sha256((dist / name).read_bytes()).hexdigest() for name in sorted(ARCHIVE_NAMES)}
    (dist / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in checksums.items()), encoding="utf-8")
    print(f"Built {len(checksums)} archives in dist/. Instructions: {len(outputs[OUTPUT_PATHS[0]])} characters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
