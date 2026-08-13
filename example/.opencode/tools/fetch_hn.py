#!/usr/bin/env python3
"""Fetch URL-bearing top stories from the public Hacker News Firebase API."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any

import requests


API_ROOT = "https://hacker-news.firebaseio.com/v0"
USER_AGENT = "tech-news-digest/1.0 (OpenCode agent team)"
DEFAULT_LIMIT = 10
MAX_LIMIT = 50


def fetch_json(session: requests.Session, url: str) -> Any:
    response = session.get(url, timeout=(10, 20))
    response.raise_for_status()
    return response.json()


def iso_timestamp(unix_timestamp: Any) -> str | None:
    if not isinstance(unix_timestamp, (int, float)):
        return None
    return datetime.fromtimestamp(unix_timestamp, timezone.utc).isoformat()


def fetch_stories(limit: int) -> dict[str, Any]:
    fetched_at = datetime.now(timezone.utc).isoformat()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})

    story_ids = fetch_json(session, f"{API_ROOT}/topstories.json")
    if not isinstance(story_ids, list):
        raise ValueError("Hacker News topstories response was not a list")

    stories: list[dict[str, Any]] = []
    for rank, story_id in enumerate(story_ids, start=1):
        if len(stories) >= limit:
            break
        if not isinstance(story_id, int):
            continue

        item = fetch_json(session, f"{API_ROOT}/item/{story_id}.json")
        if not isinstance(item, dict) or item.get("type") != "story":
            continue
        url = item.get("url")
        title = item.get("title")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        if not isinstance(title, str) or not title.strip():
            continue

        stories.append(
            {
                "rank": rank,
                "id": item.get("id", story_id),
                "title": title.strip(),
                "url": url,
                "hn_url": f"https://news.ycombinator.com/item?id={story_id}",
                "author": item.get("by"),
                "score": item.get("score"),
                "comments": item.get("descendants", 0),
                "published_at": iso_timestamp(item.get("time")),
            }
        )

    return {
        "source": "Hacker News",
        "endpoint": f"{API_ROOT}/topstories.json",
        "fetched_at": fetched_at,
        "limit": limit,
        "count": len(stories),
        "stories": stories,
    }


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: python3 fetch_hn.py [limit]", file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) == 1:
        limit = DEFAULT_LIMIT
    else:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Error: limit must be an integer", file=sys.stderr)
            sys.exit(2)
        if not 1 <= limit <= MAX_LIMIT:
            print(f"Error: limit must be between 1 and {MAX_LIMIT}", file=sys.stderr)
            sys.exit(2)

    try:
        print(json.dumps(fetch_stories(limit), ensure_ascii=False, indent=2))
    except (requests.RequestException, ValueError, OSError) as error:
        print(f"Error fetching Hacker News: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
