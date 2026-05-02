# Polish B1 Tracker

A repo-based memory system for Polish B1/ECL preparation.

The goal is not to save full chats. The goal is to keep a clean learning state that can be handed to ChatGPT at the start of every session.

## Core files

- `data/learning_state.json` — current learner state and next focus.
- `data/error_log.csv` — repeated mistakes with category and correction.
- `data/sentence_bank.md` — clean reusable B1 sentences.
- `data/session_history.md` — human-readable session history and corrected outputs.
- `data/daily_drill.md` — generated drills from repeated errors.
- `data/next_session_prompt.md` — generated prompt to paste at the start of a ChatGPT session.
- `prompts/start_session_prompt.md` — base prompt for session start.
- `prompts/end_session_json_schema.md` — JSON format ChatGPT should output at the end of a session.
- `tracker.py` — CLI to update state, generate prompts, and generate drills.

## Automation files

- `.github/ISSUE_TEMPLATE/session_update.md` — structured issue template for a learning-session update.
- `.github/workflows/process-session-issue.yml` — GitHub Action that reads session-update issues and opens a PR with updated tracker files.
- `scripts/extract_session_json_from_issue.py` — helper script that extracts one fenced JSON block from an issue body.

## Final B1 goal

Reach stable B1 exam readiness for Polish, with enough control to pass speaking, writing, reading, listening, and core grammar tasks.

Target outcomes:

- speak for 1–2 minutes on common B1 topics without collapsing;
- write two guided texts of about 100 words each;
- understand B1 reading tasks without translating every word;
- handle listening tasks with short answers and multiple choice;
- use core grammar patterns automatically enough that mistakes do not block communication;
- reuse a bank of corrected speaking/writing texts.

Current estimated level: `A2+/B1-`.

## 50-session roadmap

### Phase 1 — Grammar and output control

Goal: stop basic grammar bleeding.

- [ ] Session 1: mój / moja / moje with common nouns
- [ ] Session 2: duży / duża / duże vs dużo
- [ ] Session 3: dużo / wiele / wielu / zbyt dużo / zbyt wielu
- [ ] Session 4: genitive after dużo, nie mam, potrzebuję, szukam
- [ ] Session 5: niedaleko / blisko + genitive
- [ ] Session 6: dla + genitive: dla siebie, dla rodziny, dla mojej pracy
- [ ] Session 7: z nim / z nią / z nimi pronoun control
- [ ] Session 8: locative after w: w domu, w pracy, w mieście, w Polsce
- [ ] Session 9: instrumental for transport: autobusem, pociągiem, samochodem
- [ ] Session 10: present tense core verbs: mieszkam, pracuję, chodzę, jeżdżę, lubię
- [ ] Session 11: past tense: byłem, mieszkałem, pracowałem, pojechałem
- [ ] Session 12: future forms: będę, pojadę, chciałbym
- [ ] Session 13: connectors: ale, bo, ponieważ, dlatego, kiedy, jeśli
- [ ] Session 14: spelling drill: ż, rz, ó, u, ą, ę, ń, ć, ś, ł
- [ ] Session 15: checkpoint grammar test + update learning_state.json

Done criteria:

- learner produces 20 controlled sentences with fewer than 20% serious grammar/spelling errors;
- learner understands why the main endings change;
- learner can self-correct common mistakes.

### Phase 2 — Speaking templates

Goal: build reusable 1–2 minute monologues.

- [ ] Session 16: personal introduction + daily routine
- [ ] Session 17: city and place of living
- [ ] Session 18: apartment/house and neighborhood
- [ ] Session 19: work and professional life
- [ ] Session 20: free time and hobbies
- [ ] Session 21: sport and health
- [ ] Session 22: shopping and services
- [ ] Session 23: travel and holidays
- [ ] Session 24: family and relationships
- [ ] Session 25: friendship
- [ ] Session 26: food and restaurants
- [ ] Session 27: technology and internet
- [ ] Session 28: education and language learning
- [ ] Session 29: future plans and dreams
- [ ] Session 30: speaking checkpoint: 5 random B1 topics

Done criteria:

- learner can speak 60–90 seconds on at least 10 topics;
- learner uses beginning, development, and ending;
- learner can recover when missing a word;
- learner has at least 10 corrected monologue templates saved.

### Phase 3 — Writing exam production

Goal: write exam-style texts of about 100 words.

- [ ] Session 31: informal email — trip with friends
- [ ] Session 32: comment/opinion — friendship or city life
- [ ] Session 33: invitation / short written form
- [ ] Session 34: complaint or problem message
- [ ] Session 35: description of place/person/object
- [ ] Session 36: story/relacja from past event
- [ ] Session 37: opinion text with arguments
- [ ] Session 38: formal email basics
- [ ] Session 39: timed writing — two 100-word tasks
- [ ] Session 40: writing checkpoint + error review

Done criteria:

- learner writes two 90–110 word texts in time;
- each text answers all bullet points;
- text has greeting/closing when required;
- grammar errors do not block meaning;
- corrected texts are saved in sentence_bank/session_history.

### Phase 4 — Reading and listening exam drills

Goal: build exam speed and task familiarity.

- [ ] Session 41: B1 reading — short text multiple choice
- [ ] Session 42: B1 reading — short answers
- [ ] Session 43: B1 reading — matching and inference
- [ ] Session 44: B1 listening — short statements and intent
- [ ] Session 45: B1 listening — dialogues
- [ ] Session 46: B1 listening — interview with short answers
- [ ] Session 47: B1 listening — true/false and matching
- [ ] Session 48: grammar exam task simulation
- [ ] Session 49: full mixed mini-test
- [ ] Session 50: final readiness review and remaining risk list

Done criteria:

- learner understands task instructions without panic;
- learner answers based on text/audio, not guessing from general knowledge;
- learner can give short answers rather than full sentences when appropriate;
- learner knows time strategy.

## Current next focus

Continue from:

```text
Nie mam zbyt wielu problemów, ale mam dużo pracy.
Mam wielu klientów, ale nie mam zbyt dużo czasu.
```

Next immediate micro-topics:

1. `dużo` vs `wielu/wiele`
2. `zbyt dużo` vs `zbyt wielu`
3. `z nim` vs `z nią`
4. spelling of Polish letters
5. only then: locative after `w`

## Hard rule

Do not move to new grammar too fast. If the learner makes the same mistake twice, create an error-pattern note and drill it before adding new material.

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

## Automated issue-to-PR workflow

Use this when you want GitHub to process a session update from an issue.

1. Create a new issue using the **Polish B1 session update** template.
2. Keep the `session-update` label on the issue.
3. Paste exactly one fenced `json` block into the issue body.
4. The GitHub Action extracts the JSON, runs the tracker, and opens a PR with updated data files.
5. Review and merge the PR.

The automation intentionally opens a PR instead of pushing directly to `main`.

## Commands

```bash
python tracker.py status
python tracker.py next-prompt
python tracker.py drill
python tracker.py add-session path/to/session.json
python tracker.py windows-help
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
- `Automation` — repo/tooling improvement.

Implemented automation target:

```text
GitHub Issue with session JSON -> GitHub Action -> tracker.py add-session -> PR with updated data files
```

## Recurring GitHub update checklist

At the end of each session:

- [ ] Add new errors to `data/error_log.csv` or session issue comment.
- [ ] Add corrected reusable sentences to `data/sentence_bank.md`.
- [ ] Add clean output text to `data/session_history.md`.
- [ ] Update `data/learning_state.json` if level/focus changes.
- [ ] Regenerate `data/next_session_prompt.md`.
- [ ] Regenerate `data/daily_drill.md`.
- [ ] Commit and push, or create an issue comment if editing files is not practical.

## Why this beats raw chat memory

- The learning state is explicit.
- Repeated errors become drills.
- Clean sentences become speaking/writing templates.
- Handoff works across ChatGPT, Codex, API tools, or any future tutor.
