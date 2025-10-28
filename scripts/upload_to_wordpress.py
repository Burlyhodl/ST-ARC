#!/usr/bin/env python3
"""Upload SolarTopps blog posts to WordPress via the REST API.

This script reads the generated HTML article, extracts publishing metadata,
then uploads the post using the WordPress application password flow.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests


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
    title: str
    description: str
    slug: str


class MetadataExtractionError(RuntimeError):
    """Raised when required metadata cannot be pulled from the HTML."""


def debug_print(message: str, args: argparse.Namespace) -> None:
    """Print debug messages if not in dry-run mode."""
    if not args.dry_run:
        print(f"DEBUG: {message}", file=sys.stderr)


def extract_metadata(html: str) -> ArticleMetadata:
    """Extract the meta title, description, and slug from the HTML article."""

    print(f"DEBUG: HTML length: {len(html)} characters", file=sys.stderr)

    title_match = META_TITLE_PATTERN.search(html)
    description_match = META_DESCRIPTION_PATTERN.search(html)
    slug_match = SLUG_PATTERN.search(html)

    if not title_match:
        print("DEBUG: Available HTML preview:", html[:500], file=sys.stderr)
        raise MetadataExtractionError("Could not find <title> tag in the HTML file.")
    if not description_match:
        print("DEBUG: Available HTML preview:", html[:500], file=sys.stderr)
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


def clean_html_whitespace(value: str) -> str:
    """Collapse whitespace characters that often appear inside HTML tags."""

    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    """Generate a WordPress-friendly slug from a string."""

    lowered = value.lower()
    sanitized = re.sub(r"[^a-z0-9]+", "-", lowered)
    return sanitized.strip("-")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload a SolarTopps article to WordPress.")
    parser.add_argument(
        "file",
        help="Path to the generated HTML article that should be uploaded.",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="WordPress username that owns the application password.",
    )
    parser.add_argument(
        "--password",
        help=(
            "WordPress application password. By default the script reads "
            "WP_APPLICATION_PASSWORD from the environment."
        ),
    )
    parser.add_argument(
        "--base-url",
        default="https://www.solartopps.com",
        help="Root URL of the WordPress site (default: %(default)s).",
    )
    parser.add_argument(
        "--status",
        default="draft",
        choices=["draft", "publish", "future"],
        help="Post status for the upload (default: %(default)s).",
    )
    parser.add_argument(
        "--categories",
        type=int,
        nargs="*",
        default=None,
        help="Optional list of category IDs to assign to the post.",
    )
    parser.add_argument(
        "--tags",
        type=int,
        nargs="*",
        default=None,
        help="Optional list of tag IDs to attach to the post.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the payload instead of performing the upload.",
    )
    return parser.parse_args(argv)


def resolve_password(args: argparse.Namespace) -> str:
    if args.password:
        return args.password

    env_password = os.getenv("WP_APPLICATION_PASSWORD")
    if env_password:
        return env_password

    raise SystemExit(
        "WordPress application password not provided. Pass --password or set "
        "WP_APPLICATION_PASSWORD."
    )


def build_payload(metadata: ArticleMetadata, content: str, args: argparse.Namespace) -> Dict:
    payload: Dict[str, object] = {
        "title": metadata.title,
        "slug": metadata.slug,
        "status": args.status,
        "content": content,
        "excerpt": metadata.description,
    }

    if args.categories:
        payload["categories"] = args.categories
    if args.tags:
        payload["tags"] = args.tags

    return payload


def upload_post(
    *,
    base_url: str,
    username: str,
    password: str,
    payload: Dict[str, object],
) -> Dict:
    endpoint = base_url.rstrip("/") + "/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}

    print(f"DEBUG: Uploading to {endpoint}", file=sys.stderr)
    print(f"DEBUG: Username: {username}", file=sys.stderr)
    print(f"DEBUG: Payload keys: {list(payload.keys())}", file=sys.stderr)

    response = requests.post(
        endpoint,
        headers=headers,
        data=json.dumps(payload),
        auth=(username, password),
        timeout=30,
    )

    print(f"DEBUG: Response status: {response.status_code}", file=sys.stderr)
    print(f"DEBUG: Response headers: {dict(response.headers)}", file=sys.stderr)

    if response.status_code >= 400:
        print(f"DEBUG: Response body: {response.text}", file=sys.stderr)
        raise RuntimeError(
            f"Upload failed with status {response.status_code}: {response.text}"
        )
    return response.json()


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    print(f"DEBUG: Processing file: {args.file}", file=sys.stderr)
    print(f"DEBUG: Base URL: {args.base_url}", file=sys.stderr)
    print(f"DEBUG: Status: {args.status}", file=sys.stderr)

    try:
        with open(args.file, "r", encoding="utf-8") as file:
            html = file.read()
    except OSError as exc:
        raise SystemExit(f"Failed to read article file: {exc}") from exc

    try:
        metadata = extract_metadata(html)
    except MetadataExtractionError as exc:
        raise SystemExit(str(exc)) from exc

    payload = build_payload(metadata, html, args)

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    password = resolve_password(args)

    try:
        result = upload_post(
            base_url=args.base_url,
            username=args.username,
            password=password,
            payload=payload,
        )
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Upload failed: {exc}") from exc

    print("Upload succeeded. WordPress response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
