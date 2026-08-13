#!/usr/bin/env python3
"""Scrape article text from a Hacker News scout JSON handoff."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = "tech-news-digest/1.0 (OpenCode agent team)"
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
MAX_CONTENT_CHARS = 12_000
REQUEST_TIMEOUT = (10, 25)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def valid_url(url: Any) -> bool:
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def bounded_response_text(response: requests.Response) -> str:
    chunks: list[bytes] = []
    total = 0
    for chunk in response.iter_content(chunk_size=64 * 1024):
        if not chunk:
            continue
        remaining = MAX_RESPONSE_BYTES - total
        chunks.append(chunk[:remaining])
        total += min(len(chunk), remaining)
        if total >= MAX_RESPONSE_BYTES:
            break
    encoding = response.encoding or "utf-8"
    return b"".join(chunks).decode(encoding, errors="replace")


def truncate_text(text: str) -> tuple[str, bool]:
    if len(text) <= MAX_CONTENT_CHARS:
        return text, False
    shortened = text[:MAX_CONTENT_CHARS].rsplit(" ", 1)[0].rstrip()
    return f"{shortened}...", True


def extract_page(text: str) -> tuple[str, str, str | None, bool]:
    soup = BeautifulSoup(text, "html.parser")
    page_title = ""
    title_tag = soup.find("meta", attrs={"property": "og:title"})
    if title_tag and title_tag.get("content"):
        page_title = clean_text(str(title_tag["content"]))
    if not page_title and soup.title:
        page_title = clean_text(soup.title.get_text(" "))
    if not page_title:
        heading = soup.find("h1")
        page_title = clean_text(heading.get_text(" ")) if heading else ""

    description_tag = soup.find("meta", attrs={"name": "description"})
    description = clean_text(str(description_tag["content"])) if description_tag and description_tag.get("content") else None

    for element in soup.select("script, style, noscript, nav, header, footer, aside, form, svg, iframe"):
        element.decompose()

    container = soup.find("article") or soup.find("main") or soup.body or soup
    paragraphs: list[str] = []
    seen: set[str] = set()
    for element in container.find_all(["p", "h1", "h2", "h3"]):
        paragraph = clean_text(element.get_text(" "))
        if len(paragraph) < 30 or paragraph in seen:
            continue
        seen.add(paragraph)
        paragraphs.append(paragraph)

    content, truncated = truncate_text("\n\n".join(paragraphs))
    if not content:
        raise ValueError("no readable article paragraphs found")
    return page_title, content, description, truncated


def scrape_one(session: requests.Session, story: dict[str, Any]) -> dict[str, Any]:
    url = story.get("url")
    result: dict[str, Any] = {
        "rank": story.get("rank"),
        "id": story.get("id"),
        "title": story.get("title"),
        "url": url,
        "hn_url": story.get("hn_url"),
        "score": story.get("score"),
        "comments": story.get("comments"),
        "author": story.get("author"),
        "published_at": story.get("published_at"),
        "status": "error",
        "final_url": None,
        "page_title": None,
        "description": None,
        "content": None,
        "content_chars": 0,
        "truncated": False,
        "error": None,
    }

    if not valid_url(url):
        result["error"] = "invalid or unsupported article URL"
        return result

    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True, stream=True)
        response.raise_for_status()
        result["final_url"] = response.url
        content_type = response.headers.get("content-type", "").lower()
        if content_type and "html" not in content_type and "text/" not in content_type:
            raise ValueError(f"unsupported content type: {content_type}")
        page_text = bounded_response_text(response)
        page_title, content, description, truncated = extract_page(page_text)
        result.update(
            {
                "status": "ok",
                "page_title": page_title or None,
                "description": description,
                "content": content,
                "content_chars": len(content),
                "truncated": truncated,
                "error": None,
            }
        )
    except (requests.RequestException, ValueError, UnicodeError) as error:
        result["error"] = str(error)
    finally:
        if "response" in locals():
            response.close()
    return result


def scrape_file(input_path: Path) -> dict[str, Any]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    stories = payload.get("stories") if isinstance(payload, dict) else None
    if not isinstance(stories, list):
        raise ValueError("input JSON must contain a stories list")

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    articles = [scrape_one(session, story) for story in stories if isinstance(story, dict)]
    return {
        "source_file": str(input_path),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "count": len(articles),
        "successful": sum(article["status"] == "ok" for article in articles),
        "failed": sum(article["status"] != "ok" for article in articles),
        "articles": articles,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 scrape_articles.py <scout-json-path>", file=sys.stderr)
        sys.exit(2)

    input_path = Path(sys.argv[1])
    if not input_path.is_file():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(2)

    try:
        print(json.dumps(scrape_file(input_path), ensure_ascii=False, indent=2))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error scraping articles: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
