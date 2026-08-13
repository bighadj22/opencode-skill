---
name: source-research
description: Rules for retrieving, grading, and preserving Hacker News article sources for the daily digest.
---

# Source Research

Use this skill for the scout, researcher, and summarizer stages of the Tech News Daily Digest pipeline.

## Hacker News Discovery

- Use `https://hacker-news.firebaseio.com/v0/topstories.json` for the current ranked story IDs.
- Fetch each item from `https://hacker-news.firebaseio.com/v0/item/{id}.json`.
- Prefer `type: story` items with a public `url`, keeping the API's rank order.
- Preserve the Hacker News discussion URL even when the external page cannot be fetched.
- Record API metadata such as title, author, score, descendants, item ID, and timestamps exactly as returned.

## Article Retrieval

- Request only `http` and `https` article URLs.
- Use a descriptive user agent, bounded timeouts, and a bounded response size.
- Remove navigation, scripts, styles, forms, and other boilerplate before extracting paragraphs.
- Prefer an `article` or `main` element, then fall back to the page body.
- Preserve the final redirected URL and record HTTP or parsing failures per article.

## Evidence Rules

- A fact belongs in a summary only when it is supported by extracted article text.
- The title and Hacker News metadata are context, not evidence for claims about article contents.
- Treat missing, blocked, paywalled, empty, and non-HTML pages as unavailable.
- Never fill gaps with general knowledge, guesses, or other articles.
