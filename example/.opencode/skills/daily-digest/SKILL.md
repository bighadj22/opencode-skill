---
name: daily-digest
description: Shared schema, Markdown structure, and editorial rules for the Tech News Daily Digest.
---

# Daily Digest

Use this skill for summary JSON, curation, and publication validation.

## Summary Handoff Schema

The summarizer writes an object with:

```json
{
  "generated_at": "ISO-8601 UTC timestamp",
  "source_file": "research handoff path",
  "summaries": [
    {
      "rank": 1,
      "title": "Original Hacker News title",
      "url": "https://source.example/article",
      "hn_url": "https://news.ycombinator.com/item?id=123",
      "score": 100,
      "comments": 25,
      "published_at": "ISO-8601 UTC timestamp or null",
      "status": "ok",
      "summary": "Exactly two or three source-grounded sentences.",
      "note": null
    }
  ]
}
```

For an unavailable source, use `status: "unavailable"`, `summary: null`, and a non-empty `note`.

## Markdown Structure

The curator writes:

1. `# Daily Tech Digest`
2. The UTC date and a one-line introduction
3. One `##` section per story in rank order, with the original title linked to the source
4. The 2-3 sentence summary
5. A metadata line containing the Hacker News discussion link, score, and comments when available
6. A `## Coverage Notes` section only when one or more sources were unavailable

## Editorial Rules

- Keep the writing concise, neutral, and useful.
- Preserve original titles and URLs; do not create tracking parameters.
- Never turn unavailable content into a guessed summary.
- Do not add advertisements, opinions, affiliate links, or unsupported claims.
- Keep valid Markdown and ensure links use absolute `https://` or `http://` URLs.
