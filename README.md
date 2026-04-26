# Polish B1 Tracker

A repo-based memory system for Polish B1/ECL preparation.

The goal is not to save full chats. The goal is to keep a clean learning state that can be handed to ChatGPT at the start of every session.

## Core files

- `data/learning_state.json` — current learner state and next focus.
- `data/error_log.csv` — repeated mistakes with category and correction.
- `data/sentence_bank.md` — clean reusable B1 sentences.
- `data/session_history.md` — human-readable session log.
- `data/daily_drill.md` — generated drills from repeated errors.
- `data/next_session_prompt.md` — generated prompt to paste at the start of a ChatGPT session.
- `prompts/start_session_prompt.md` — base prompt for session start.
- `prompts/end_session_json_schema.md` — JSON format ChatGPT should output at the end of a session.
- `tracker.py` — CLI to update state, generate prompts, and generate drills.

## Daily workflow

At the start of a learning session:

```bash
git pull
python tracker.py status
python tracker.py next-prompt
```

Then paste `data/next_session_prompt.md` into ChatGPT.

At the end of a learning session:

1. Ask ChatGPT: `Prepare the session JSON for my Polish B1 tracker.`
2. Save the JSON as `session_YYYY-MM-DD.json`.
3. Run:

```bash
python tracker.py add-session session_YYYY-MM-DD.json
python tracker.py next-prompt
python tracker.py drill
git add .
git commit -m "Add Polish B1 session update"
git push origin main
```

## Commands

```bash
python tracker.py status
python tracker.py next-prompt
python tracker.py drill
python tracker.py add-session path/to/session.json
python -m unittest discover tests
```

## Windows encoding fix

If Polish characters appear as broken text such as `┼ø`, set the terminal to UTF-8 before reading files:

```bat
chcp 65001
type data\next_session_prompt.md
```

Better options:

- open files in VS Code using UTF-8,
- use Windows Terminal or PowerShell with UTF-8,
- avoid copying Polish text from a non-UTF-8 console.

## Issue-based learning workflow

Use GitHub Issues for session planning and backlog, not for raw chat dumps.

Recommended issue types:

- `Session: Day X` — contains one session JSON and learning notes.
- `Error Pattern` — repeated grammar/spelling problem to drill.
- `Output Text` — clean speaking or writing text to reuse.
- `Automation` — engineering task for tracker improvements.

Long-term automation target:

```text
GitHub Issue with session JSON -> GitHub Action -> tracker.py add-session -> PR with updated data files
```

## Why this beats raw chat memory

- The learning state is explicit.
- Repeated errors become drills.
- Clean sentences become speaking/writing templates.
- Handoff works across ChatGPT, Codex, API tools, or any future tutor.
