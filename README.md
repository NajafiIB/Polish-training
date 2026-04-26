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

## Workflow

1. Practice with ChatGPT.
2. At the end, ask ChatGPT for a session JSON using `prompts/end_session_json_schema.md`.
3. Save that JSON locally, for example `session_2026-04-26.json`.
4. Run:

```bash
python tracker.py add-session session_2026-04-26.json
python tracker.py next-prompt
python tracker.py drill
```

5. Paste `data/next_session_prompt.md` into the next ChatGPT session.

## Commands

```bash
python tracker.py status
python tracker.py next-prompt
python tracker.py drill
python tracker.py add-session path/to/session.json
python -m unittest discover tests
```

## Why this beats raw chat memory

- The learning state is explicit.
- Repeated errors become drills.
- Clean sentences become speaking/writing templates.
- Handoff works across ChatGPT, Codex, API tools, or any future tutor.
