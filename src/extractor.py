#!/usr/bin/env python3
"""
extractor.py
============

Runs every regex in ``patterns.py`` over a block of text (or a text file) and
reports what was found.

Usage (from the project root)::

    python -m src.extractor                       # uses data/sample_input.txt
    python -m src.extractor path/to/file.txt      # custom input file
    python -m src.extractor --json                # machine-readable output
    python -m src.extractor --save output/sample_output.txt
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

from src.patterns import PATTERNS

DEFAULT_INPUT = Path("data/sample_input.txt")


def extract_all(text: str) -> Dict[str, List[str]]:
    """Return ``{data_type: [matches, ...]}`` for every registered pattern.

    ``m.group(0)`` is used (instead of ``findall``) because some patterns
    contain capture groups, and ``findall`` would return only the group
    contents rather than the full match.
    """
    return {
        name: [m.group(0) for m in pattern.finditer(text)]
        for name, pattern in PATTERNS.items()
    }


def extract_from_file(path: Path) -> Dict[str, List[str]]:
    """Read a UTF-8 text file and run :func:`extract_all` on its contents."""
    return extract_all(Path(path).read_text(encoding="utf-8"))


def format_report(results: Dict[str, List[str]]) -> str:
    """Build a human-readable report from the extraction results."""
    lines = []
    for name, matches in results.items():
        lines.append(f"{name.upper().replace('_', ' ')} ({len(matches)} found)")
        lines.extend(f"  - {m}" for m in matches)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract emails, URLs, phones, cards, times, HTML tags, "
                    "hashtags and currency amounts from text."
    )
    parser.add_argument("input", nargs="?", default=str(DEFAULT_INPUT),
                        help="path to the text file (default: data/sample_input.txt)")
    parser.add_argument("--json", action="store_true",
                        help="print results as JSON")
    parser.add_argument("--save", metavar="FILE",
                        help="also write the report to FILE")
    args = parser.parse_args(argv)

    try:
        results = extract_from_file(Path(args.input))
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1

    report = json.dumps(results, indent=2) if args.json else format_report(results)
    print(report)

    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Report saved to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
