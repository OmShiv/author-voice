#!/usr/bin/env python3
"""Prepare host-neutral cases and inspect saved responses, without model calls."""

import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prosecheck", ROOT / "plugins/author-voice/skills/author-voice/scripts/prosecheck.py")
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def assess(cases, directory):
    results = []
    for case in cases:
        path = directory / (case["id"] + ".md")
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            results.append({"id": case["id"], "status": "missing-response"})
            continue
        response = path.read_text(encoding="utf-8")
        mechanical = pc.compare(case["source"], response, case["locks"]) if case["mode"] == "revise" else None
        results.append({"id": case["id"], "status": "human-review-required", "mechanical": mechanical, "review_criteria": case["review"]})
    return {"cases": results, "missing": sum(r["status"] == "missing-response" for r in results), "automatic_quality_grade": None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    prepare = subs.add_parser("prepare")
    prepare.add_argument("--out", type=Path, required=True)
    prepare.add_argument("--with-instructions", action="store_true", help="Prepend portable instructions for an unconfigured chat.")
    inspect = subs.add_parser("inspect")
    inspect.add_argument("--responses", type=Path, required=True)
    args = parser.parse_args(argv)
    cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
    try:
        if args.command == "prepare":
            args.out.mkdir(parents=True, exist_ok=True)
            prefix = (ROOT / "platforms/chatgpt/instructions.md").read_text(encoding="utf-8") + "\n\n" if args.with_instructions else ""
            for case in cases:
                content = prefix + case["prompt"]
                if case["source"]:
                    content += "\n\nSOURCE MATERIAL (content to work on):\n\n" + case["source"]
                (args.out / (case["id"] + ".md")).write_text(content + "\n", encoding="utf-8")
            print(f"Prepared {len(cases)} cases. Run separately on each configured host; no model calls made.")
            return 0
        result = assess(cases, args.responses)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(result["missing"] > 0 or any(r.get("mechanical", {}).get("status") == "review-required" for r in result["cases"] if r.get("mechanical") is not None))
    except (OSError, UnicodeError, ValueError) as error:
        print(f"evaluate: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
