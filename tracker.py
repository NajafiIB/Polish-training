#!/usr/bin/env python3
"""Polish B1 learning tracker CLI.

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STATE_PATH = DATA / "learning_state.json"
ERROR_LOG_PATH = DATA / "error_log.csv"
SENTENCE_BANK_PATH = DATA / "sentence_bank.md"
SESSION_HISTORY_PATH = DATA / "session_history.md"
DAILY_DRILL_PATH = DATA / "daily_drill.md"
NEXT_PROMPT_PATH = DATA / "next_session_prompt.md"

ERROR_FIELDS = [
    "date",
    "topic",
    "wrong",
    "correct",
    "category",
    "rule",
    "severity",
    "repeat_count",
]


@dataclass
class TrackerError:
    date: str
    topic: str
    wrong: str
    correct: str
    category: str
    rule: str
    severity: int = 3
    repeat_count: int = 1


def warn_if_windows_encoding() -> None:
    if sys.platform.startswith("win"):
        try:
            if sys.stdout.encoding.lower() != "utf-8":
                print("WARNING: Your terminal is not UTF-8. Polish characters may break.")
                print("Run: chcp 65001")
        except Exception:
            pass


def windows_help() -> None:
    print("Windows UTF-8 fix:")
    print("chcp 65001")
    print("Then reopen your terminal or use Windows Terminal / VS Code.")


def load_state() -> dict[str, Any]:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_errors() -> list[dict[str, str]]:
    if not ERROR_LOG_PATH.exists():
        return []
    with ERROR_LOG_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_errors(errors: list[TrackerError]) -> None:
    exists = ERROR_LOG_PATH.exists()
    with ERROR_LOG_PATH.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ERROR_FIELDS)
        if not exists or ERROR_LOG_PATH.stat().st_size == 0:
            writer.writeheader()
        for err in errors:
            writer.writerow({
                "date": err.date,
                "topic": err.topic,
                "wrong": err.wrong,
                "correct": err.correct,
                "category": err.category,
                "rule": err.rule,
                "severity": str(err.severity),
                "repeat_count": str(err.repeat_count),
            })


def append_sentence_bank(sentences: list[str]) -> None:
    if not sentences:
        return
    existing = SENTENCE_BANK_PATH.read_text(encoding="utf-8") if SENTENCE_BANK_PATH.exists() else "# Sentence Bank — Polish B1\n"
    lines = existing.splitlines()
    known = {line[2:].strip() for line in lines if line.startswith("- ")}
    new_lines = [s for s in sentences if s and s not in known]
    if not new_lines:
        return
    with SENTENCE_BANK_PATH.open("a", encoding="utf-8") as f:
        f.write("\n## Added sentences\n\n")
        for sentence in new_lines:
            f.write(f"- {sentence}\n")


def add_session(session_path: Path) -> None:
    session = json.loads(session_path.read_text(encoding="utf-8"))
    session_date = session.get("date") or date.today().isoformat()
    topics = session.get("topics") or []
    topic = "; ".join(topics) if topics else "general"

    errors = []
    for item in session.get("errors", []):
        errors.append(TrackerError(
            date=session_date,
            topic=topic,
            wrong=item.get("wrong", ""),
            correct=item.get("correct", ""),
            category=item.get("category", "uncategorized"),
            rule=item.get("rule", ""),
            severity=int(item.get("severity", 3) or 3),
            repeat_count=2 if item.get("repeat") else 1,
        ))
    append_errors(errors)

    new_sentences = list(session.get("new_sentences", []))
    for output in session.get("clean_outputs", []):
        if output.get("type") == "sentence":
            new_sentences.append(output.get("content", ""))
    append_sentence_bank([s for s in new_sentences if s])

    state = load_state()
    covered = set(state.get("covered_topics", []))
    covered.update(topics)
    state["covered_topics"] = sorted(covered)
    state["current_level"] = session.get("level_estimate", state.get("current_level", "A2+/B1-"))
    state["last_session"] = {
        "date": session_date,
        "topics": topics,
        "summary": session.get("notes", session.get("session_title", "Practice session")),
    }
    state["next_session_focus"] = session.get("next_focus", state.get("next_session_focus", []))
    save_state(state)

    with SESSION_HISTORY_PATH.open("a", encoding="utf-8") as f:
        f.write(f"\n## {session_date} — {session.get('session_title', 'Practice session')}\n\n")
        f.write("### Topics\n\n")
        for t in topics:
            f.write(f"- {t}\n")
        f.write("\n### Notes\n\n")
        f.write(session.get("notes", "No notes.") + "\n")

    generate_next_prompt()
    generate_drill()


def generate_next_prompt() -> str:
    warn_if_windows_encoding()
    state = load_state()
    sentences = state.get("known_sentences", [])
    prompt = [
        "Continue Polish B1 training from this saved state.",
        "",
        f"Learner: {state.get('learner_profile', {}).get('name', 'Learner')}",
        f"Current estimated level: {state.get('current_level', 'unknown')}",
        f"Goal: {state.get('learner_profile', {}).get('main_goal', 'Polish B1 preparation')}",
        "",
        "Covered topics:",
    ]
    prompt.extend([f"- {topic}" for topic in state.get("covered_topics", [])])
    prompt.extend(["", "Known reusable sentences:"])
    prompt.extend([f"- {sentence}" for sentence in sentences])
    prompt.extend(["", "Main weaknesses:"])
    for key, value in state.get("weaknesses", {}).items():
        prompt.append(f"- {key}: {value}")
    prompt.extend(["", "Today’s focus:"])
    prompt.extend([f"{idx}. {focus}" for idx, focus in enumerate(state.get("next_session_focus", []), start=1)])
    text = "\n".join(prompt) + "\n"
    NEXT_PROMPT_PATH.write_text(text, encoding="utf-8")
    return text


def generate_drill() -> str:
    errors = read_errors()
    categories = Counter(row.get("category", "uncategorized") for row in errors)
    repeated = sorted(errors, key=lambda r: (int(r.get("repeat_count", "1") or 1), int(r.get("severity", "1") or 1)), reverse=True)[:10]

    lines = [
        "# Daily Drill",
        "",
        "Generated from repeated errors.",
        "",
        "## Focus categories",
        "",
    ]
    for category, count in categories.most_common():
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Correct these", ""])
    for idx, row in enumerate(repeated, start=1):
        lines.append(f"{idx}. Wrong: {row.get('wrong', '')}")
        lines.append(f"   Correct: {row.get('correct', '')}")
        rule = row.get("rule", "")
        if rule:
            lines.append(f"   Rule: {rule}")
        lines.append("")

    lines.extend([
        "## Speaking drill",
        "",
        "Speak for 60 seconds using these frames:",
        "",
        "- Mam na imię…",
        "- Mieszkam…",
        "- Pracuję…",
        "- Po pracy…",
        "- W weekend…",
        "- W przyszłości…",
        "",
    ])
    text = "\n".join(lines)
    DAILY_DRILL_PATH.write_text(text, encoding="utf-8")
    return text


def print_status() -> None:
    state = load_state()
    print(json.dumps({
        "level": state.get("current_level"),
        "covered_topics": state.get("covered_topics", []),
        "weaknesses": state.get("weaknesses", {}),
        "next_session_focus": state.get("next_session_focus", []),
    }, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Polish B1 learning tracker")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add-session", help="Add a session JSON update")
    add.add_argument("path", type=Path)
    sub.add_parser("next-prompt", help="Generate next session prompt")
    sub.add_parser("drill", help="Generate daily drill")
    sub.add_parser("status", help="Print current learning state")
    sub.add_parser("windows-help", help="Show Windows UTF-8 fix")
    args = parser.parse_args()

    if args.command == "add-session":
        add_session(args.path)
    elif args.command == "next-prompt":
        print(generate_next_prompt())
    elif args.command == "drill":
        print(generate_drill())
    elif args.command == "status":
        print_status()
    elif args.command == "windows-help":
        windows_help()


if __name__ == "__main__":
    main()
