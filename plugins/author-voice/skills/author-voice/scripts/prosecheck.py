#!/usr/bin/env python3
"""Conservative, offline editorial checks. Never a detector or semantic validator."""

from __future__ import annotations

import argparse
from collections import Counter
import difflib
import json
from pathlib import Path
import re
import sys


NUMBER = re.compile(r"(?<![\w])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+−]?\d+)?(?:[%‰])?(?!\w)")
QUANTITY = re.compile(
    r"(?<!\w)[-+−]?\d+(?:\.\d+)?\s*(?:µs|μs|ns|ms|s|min|h|Hz|kHz|MHz|GHz|"
    r"B|kB|KB|MB|GB|TB|KiB|MiB|GiB|TiB|nm|mm|cm|m|km|mg|kg|g|mL|L|K|°C|W|kW|J|kJ|V|mV|Pa|kPa)(?!\w)"
)
PATTERNS = {
    "keep_blocks": re.compile(r"<!--\s*author-voice:keep\s*-->[\s\S]*?<!--\s*/author-voice:keep\s*-->"),
    "inline_code": re.compile(r"(?<!`)(`+)(?!`)([^\n]*?)(?<!`)\1(?!`)"),
    "math": re.compile(r"\$\$[\s\S]*?\$\$|(?<![\\$])\$(?!\$)[^\n$]+?(?<!\\)\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\\begin\{(equation\*?|align\*?|gather\*?)\}[\s\S]*?\\end\{\1\}"),
    "citations": re.compile(r"\[(?:\d+(?:\s*[,;–−-]\s*\d+)*|[^\]\n]*@[\w][^\]\n]*)\]|\\(?:[A-Za-z]*cite[A-Za-z]*|ref|eqref|label)\*?(?:\[[^\]]*\])*\{[^}]*\}|\[\^[^\]\n]+\]|\([^()\n]*\b(?:18|19|20)\d{2}[a-z]?[^()\n]*\)"),
    "link_targets": re.compile(r"!?\[[^\]\n]*\]\((?:[^()\n]|\([^()\n]*\))*\)|https?://[^\s<>\]\)]+"),
    "quotations": re.compile(r'"[^"\n]+"|“[^”\n]+”|‘[^’\n]+’'),
    "blockquotes": re.compile(r"^ {0,3}>.*$", re.MULTILINE),
    "headings": re.compile(r"^ {0,3}#{1,6}\s+.*$|^[^\n]+\n(?:={3,}|-{3,})\s*$", re.MULTILINE),
    "table_rows": re.compile(r"^[ \t]*\|.*\|[ \t]*$", re.MULTILINE),
    "reference_definitions": re.compile(r"^ {0,3}\[[^\]\n]+\]:[^\n]*(?:\n(?: {4}|\t)[^\n]*)*", re.MULTILINE),
}
STOCK = re.compile(r"\b(?:it is worth noting that|in today's (?:rapidly evolving|ever-changing) (?:world|landscape)|delve into|a testament to|plays a pivotal role|in conclusion|furthermore|moreover|seamlessly)\b", re.I)
QUALIFIER = re.compile(r"\b(?:not|no|never|may|might|could|associated|association|causes?|causal|only|approximately|suggests?|significant|non-significant)\b", re.I)


def fenced_blocks(text: str) -> list[str]:
    blocks, current = [], []
    marker, length = None, 0
    for line in text.splitlines(keepends=True):
        if marker is None:
            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
            if match:
                marker, length = match[1][0], len(match[1])
                current = [line]
        else:
            current.append(line)
            if re.fullmatch(r" {0,3}" + re.escape(marker) + r"{" + str(length) + r",}[ \t]*(?:\r?\n)?", line):
                blocks.append("".join(current))
                marker, current = None, []
    if current:
        blocks.append("".join(current))
    return blocks


def extract(text: str) -> dict[str, list[str]]:
    items = {"numbers": NUMBER.findall(text), "quantities": QUANTITY.findall(text), "code_fences": fenced_blocks(text)}
    # Keep duplicates: losing the second occurrence of a result is a difference.
    for kind, pattern in PATTERNS.items():
        items[kind] = [match.group(0) for match in pattern.finditer(text)]
    return items


def counter_delta(before: list[str], after: list[str]) -> dict:
    left, right = Counter(before), Counter(after)
    return {"removed": list((left - right).elements()), "added": list((right - left).elements())}


def compare(before: str, after: str, locks: list[str] | None = None) -> dict:
    original, revised = extract(before), extract(after)
    differences = {}
    for kind in original:
        delta = counter_delta(original[kind], revised[kind])
        if delta["removed"] or delta["added"]:
            differences[kind] = delta
    for phrase in locks or []:
        if phrase not in before:
            raise ValueError(f"Protected string not found in original: {phrase!r}")
        if before.count(phrase) != after.count(phrase):
            differences.setdefault("explicit_locks", []).append({"text": phrase, "before": before.count(phrase), "after": after.count(phrase)})
    qualifiers = counter_delta([x.lower() for x in QUALIFIER.findall(before)], [x.lower() for x in QUALIFIER.findall(after)])
    notes = []
    if qualifiers["removed"] or qualifiers["added"]:
        notes.append({"kind": "qualifiers", "message": "Review changes in uncertainty, negation, or causal language in context.", **qualifiers})
    return {
        "status": "review-required" if differences or notes else "no-mechanical-differences-found",
        "protected_differences": differences,
        "review_notes": notes,
        "semantic_review_required": True,
        "limits": "Lexical checks only. Equal tokens do not prove equal meaning, citation support, ordering, or completeness. Markdown/LaTeX parsing is partial; bibliography prose and many units need explicit locks or manual review.",
    }


def lint(text: str) -> dict:
    # Mask literal material while retaining original offsets and line numbers.
    masked = text
    for literal in fenced_blocks(text):
        masked = masked.replace(literal, re.sub(r"[^\n]", " ", literal))
    for kind in ("keep_blocks", "inline_code", "math", "quotations", "blockquotes", "reference_definitions"):
        masked = PATTERNS[kind].sub(lambda m: re.sub(r"[^\n]", " ", m.group()), masked)
    candidates = [
        {"line": masked.count("\n", 0, m.start()) + 1, "text": m.group(), "reason": "Keep if it adds meaning; otherwise consider a direct subject and verb."}
        for m in STOCK.finditer(masked)
    ]
    return {"candidates": candidates, "advisory_only": True, "limits": "A phrase match is not evidence of AI authorship or a mandatory edit. No score or automatic replacements."}


def read_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() not in {".md", ".markdown", ".txt", ".tex"}:
        raise ValueError("Use a UTF-8 .md, .markdown, .txt, or .tex source, not a PDF or Word file.")
    return p.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    lp = commands.add_parser("lint", help="List a few editorial candidates; never rewrite.")
    lp.add_argument("file")
    lp.add_argument("--json", action="store_true")
    cp = commands.add_parser("compare", help="Compare protected lexical material; exit 1 means review needed.")
    cp.add_argument("original")
    cp.add_argument("revised")
    cp.add_argument("--locks", help="Path to a JSON array of additional exact strings to protect.")
    cp.add_argument("--json", action="store_true")
    cp.add_argument("--diff", action="store_true", help="Include a unified text diff (text output only).")
    args = parser.parse_args(argv)
    try:
        if args.command == "lint":
            result = lint(read_text(args.file))
        else:
            locks = json.loads(Path(args.locks).read_text(encoding="utf-8")) if args.locks else []
            if not isinstance(locks, list) or any(not isinstance(s, str) or not s for s in locks):
                raise ValueError("Locks must be a JSON array of nonempty strings.")
            before, after = read_text(args.original), read_text(args.revised)
            result = compare(before, after, locks)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"prosecheck: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if args.command == "lint":
            for candidate in result["candidates"]:
                print(f"Line {candidate['line']}: {candidate['text']} — {candidate['reason']}")
            print(f"{len(result['candidates'])} editorial candidate(s). {result['limits']}")
        else:
            print(result["status"])
            for kind, delta in result["protected_differences"].items():
                print(f"{kind}: {json.dumps(delta, ensure_ascii=False)}")
            for note in result["review_notes"]:
                print(json.dumps(note, ensure_ascii=False))
            print(result["limits"])
            if args.diff:
                sys.stdout.writelines(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True), fromfile=args.original, tofile=args.revised))
    return int(args.command == "compare" and result["status"] == "review-required")


if __name__ == "__main__":
    raise SystemExit(main())
