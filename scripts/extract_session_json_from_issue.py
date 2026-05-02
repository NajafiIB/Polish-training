#!/usr/bin/env python3
"""Extract a fenced JSON block from a GitHub issue body.

Usage:
    python scripts/extract_session_json_from_issue.py issue_body.md session.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def extract_json_block(text: str) -> str:
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No fenced ```json ... ``` block found in issue body.")
    raw = match.group(1)
    json.loads(raw)
    return json.dumps(json.loads(raw), ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: extract_session_json_from_issue.py issue_body.md session.json")
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    text = input_path.read_text(encoding="utf-8")
    output_path.write_text(extract_json_block(text), encoding="utf-8")


if __name__ == "__main__":
    main()
