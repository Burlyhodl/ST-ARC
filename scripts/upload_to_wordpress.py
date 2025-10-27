#!/usr/bin/env python3
"""Upload SolarTopps blog posts to WordPress via the REST API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from st_arc.env import load_env
from st_arc.wordpress import (
    MetadataExtractionError,
    build_payload,
    extract_metadata,
    load_html,
    upload_post,
)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload a SolarTopps article to WordPress.")
    parser.add_argument(
        "file",
        help="Path to the generated HTML article that should be uploaded.",
    )
    parser.add_argument(
        "--env-file",
        help="Path to a .env file to load before running. Defaults to project .env if present.",
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
def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    try:
        load_env(args.env_file, overwrite=bool(args.env_file))
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc

    try:
        html = load_html(args.file)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    try:
        metadata = extract_metadata(html)
    except MetadataExtractionError as exc:
        raise SystemExit(str(exc)) from exc

    payload = build_payload(
        metadata,
        html,
        status=args.status,
        categories=args.categories,
        tags=args.tags,
    )

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
