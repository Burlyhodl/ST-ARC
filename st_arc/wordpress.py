"""Helpers for reading SolarTopps HTML articles and uploading them to WordPress."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

META_TITLE_PATTERN = re.compile(r"<title>(?P<title>.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESCRIPTION_PATTERN = re.compile(
    r'<meta\s+name="description"\s+content="(?P<description>.*?)"\s*/?>',
    re.IGNORECASE | re.DOTALL,
)
SLUG_PATTERN = re.compile(
    r"<strong>\s*Slug:\s*</strong>\s*(?P<slug>[^<]+)", re.IGNORECASE | re.DOTALL
)


@dataclass
class ArticleMetadata:
    """Container for the key WordPress metadata embedded in the HTML export."""

    title: str
    description: str
    slug: str


class MetadataExtractionError(RuntimeError):
    """Raised when required metadata cannot be pulled from the HTML."""


def clean_html_whitespace(value: str) -> str:
    """Collapse whitespace characters that often appear inside HTML tags."""

    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    """Generate a WordPress-friendly slug from a string."""

    lowered = value.lower()
    sanitized = re.sub(r"[^a-z0-9]+", "-", lowered)
    return sanitized.strip("-")


def extract_metadata(html: str) -> ArticleMetadata:
    """Extract the meta title, description, and slug from the HTML article."""

    title_match = META_TITLE_PATTERN.search(html)
    description_match = META_DESCRIPTION_PATTERN.search(html)
    slug_match = SLUG_PATTERN.search(html)

    if not title_match:
        raise MetadataExtractionError("Could not find <title> tag in the HTML file.")
    if not description_match:
        raise MetadataExtractionError(
            "Could not find meta description. Ensure a <meta name=\"description\"> tag exists."
        )

    if slug_match:
        slug = slug_match.group("slug").strip()
    else:
        slug = slugify(title_match.group("title"))

    return ArticleMetadata(
        title=clean_html_whitespace(title_match.group("title")),
        description=clean_html_whitespace(description_match.group("description")),
        slug=slug,
    )


def load_html(path: str | Path) -> str:
    """Read an article from disk and return the HTML contents."""

    article_path = Path(path)
    try:
        return article_path.read_text(encoding="utf-8")
    except OSError as exc:  # noqa: PLE0704
        raise RuntimeError(f"Failed to read article file '{article_path}': {exc}") from exc


def build_payload(
    metadata: ArticleMetadata,
    content: str,
    *,
    status: str,
    categories: Optional[Iterable[int]] = None,
    tags: Optional[Iterable[int]] = None,
) -> Dict[str, object]:
    """Compose the JSON payload expected by the WordPress posts endpoint."""

    payload: Dict[str, object] = {
        "title": metadata.title,
        "slug": metadata.slug,
        "status": status,
        "content": content,
        "excerpt": metadata.description,
    }

    if categories:
        payload["categories"] = list(categories)
    if tags:
        payload["tags"] = list(tags)

    return payload


def upload_post(
    *,
    base_url: str,
    username: str,
    password: str,
    payload: Dict[str, object],
    timeout: int = 30,
) -> Dict[str, object]:
    """Send the post payload to WordPress via the REST API."""

    import requests

    endpoint = base_url.rstrip("/") + "/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        endpoint,
        headers=headers,
        data=json.dumps(payload),
        auth=(username, password),
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Upload failed with status {response.status_code}: {response.text}"
        )
    return response.json()
