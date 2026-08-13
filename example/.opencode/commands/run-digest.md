---
description: Run the complete Tech News Daily Digest pipeline
agent: coordinator
model: opencode/deepseek-v4-flash-free
---

Run the complete Tech News Daily Digest pipeline for `$ARGUMENTS`.

If no argument is provided, fetch the current top 10 URL-bearing Hacker News stories. Delegate scout, researcher, summarizer, curator, and publisher in order. Report each handoff path and stop on any failure.
