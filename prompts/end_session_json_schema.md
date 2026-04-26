# End Session JSON Schema

At the end of every ChatGPT practice session, output a JSON object with this exact shape:

```json
{
  "date": "YYYY-MM-DD",
  "session_title": "short title",
  "topics": ["topic 1", "topic 2"],
  "skills_practiced": ["speaking", "writing", "reading", "grammar"],
  "clean_outputs": [
    {
      "type": "speaking_script|writing_sample|sentence",
      "title": "short title",
      "content": "corrected Polish text"
    }
  ],
  "errors": [
    {
      "wrong": "learner version",
      "correct": "correct version",
      "category": "case|verb|spelling|preposition|word_choice|structure|agreement|reflexive_verb",
      "rule": "short rule",
      "severity": 1,
      "repeat": true
    }
  ],
  "new_sentences": ["clean reusable sentence"],
  "level_estimate": "A2+/B1-",
  "next_focus": ["focus 1", "focus 2"],
  "notes": "brief trainer note"
}
```

Rules:
- Include only meaningful repeated errors, not every typo.
- Include only clean Polish outputs worth memorizing.
- Keep the JSON valid.
