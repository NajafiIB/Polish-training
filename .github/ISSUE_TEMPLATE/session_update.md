---
name: Polish B1 session update
about: Add a structured Polish B1 learning session update
title: "Session: YYYY-MM-DD — Topic"
labels: session-update
---

## Instructions

Do not paste full raw chat logs. Save only corrected outputs, repeated errors, reusable sentences, level estimate, and next focus.

Paste one valid JSON block below.

```json
{
  "date": "YYYY-MM-DD",
  "session_title": "Day X — Topic",
  "topics": ["topic 1", "topic 2"],
  "clean_outputs": [
    {
      "type": "monologue",
      "title": "Title",
      "content": "Corrected Polish text here."
    }
  ],
  "new_sentences": [
    "Correct reusable sentence."
  ],
  "errors": [
    {
      "wrong": "wrong form",
      "correct": "correct form",
      "category": "case",
      "rule": "short rule",
      "severity": 5,
      "repeat": true
    }
  ],
  "level_estimate": "A2+/B1-",
  "next_focus": [
    "focus 1",
    "focus 2"
  ],
  "notes": "Short session summary."
}
```
