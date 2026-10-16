"""CLI for PhishNet."""

from __future__ import annotations

import argparse
import json
import sys

from .service import analyze_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phishnet")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_parser = sub.add_parser("analyze", help="Analyze a URL or message")
    analyze_parser.add_argument("value", help="URL or message to analyze")
    analyze_parser.add_argument(
        "--type", choices=["url", "message"], default="url", dest="input_type"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        if args.input_type == "url":
            result = analyze_input(url=args.value)
        else:
            result = analyze_input(message=args.value)
        print(json.dumps(result.model_dump(), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
