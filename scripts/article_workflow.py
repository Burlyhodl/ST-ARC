#!/usr/bin/env python3
"""End-to-end CLI for generating and uploading SolarTopps articles."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from st_arc.env import load_env
from st_arc.generator import ArticleRequest, SolarArticleGenerator, fetch_reference_source
from st_arc.wordpress import (
    MetadataExtractionError,
    build_payload,
    extract_metadata,
    load_html,
    upload_post,
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SolarTopps-branded blog posts and optionally upload them to WordPress.",
    )
    parser.add_argument(
        "--env-file",
        help="Path to a .env file to load before running commands. Defaults to project .env if present.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser(
        "generate",
        help="Create a new article using the OpenAI Responses API.",
    )
    add_generation_arguments(generate)
    add_upload_arguments(generate, optional=True, include_file=False)

    publish = subparsers.add_parser(
        "publish",
        help="Upload an existing HTML article to WordPress.",
    )
    add_upload_arguments(publish, optional=False, include_file=True)

    return parser.parse_args(argv)


def add_generation_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("keyword", help="Primary keyword for the SEO article.")
    parser.add_argument(
        "--reference-url",
        help="URL for the reference article or source inspiration.",
    )
    parser.add_argument(
        "--reference-file",
        help="Local file containing the reference article.",
    )
    parser.add_argument(
        "--reference-text",
        help="Raw reference article text pasted directly via CLI.",
    )
    parser.add_argument(
        "--secondary-keywords",
        nargs="*",
        help="Optional list of secondary keywords to include.",
    )
    parser.add_argument(
        "--focus-topic",
        help="Specific theme or angle to emphasize in the article.",
    )
    parser.add_argument(
        "--chart-data",
        help="JSON or descriptive text for the chart placeholder.",
    )
    parser.add_argument(
        "--meta-title",
        help="Preferred meta title. Generated automatically if omitted.",
    )
    parser.add_argument(
        "--meta-description",
        help="Preferred meta description under 155 characters.",
    )
    parser.add_argument(
        "--slug",
        help="Custom slug to embed in the article metadata.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4.1-mini",
        help="OpenAI model used for article generation (default: %(default)s).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature for the model (default: %(default)s).",
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key. Falls back to OPENAI_API_KEY environment variable.",
    )
    parser.add_argument(
        "--output",
        help="Destination file for the generated HTML. Defaults to content/<slug>.html.",
    )


def add_upload_arguments(
    parser: argparse.ArgumentParser, *, optional: bool, include_file: bool
) -> None:
    required_flag = not optional
    if include_file:
        parser.add_argument(
            "--file",
            required=required_flag,
            help="Path to the HTML file that should be uploaded to WordPress.",
        )
    parser.add_argument(
        "--username",
        required=required_flag,
        help="WordPress username associated with the application password.",
    )
    parser.add_argument(
        "--password",
        help="WordPress application password. Falls back to WP_APPLICATION_PASSWORD.",
    )
    parser.add_argument(
        "--base-url",
        default="https://www.solartopps.com",
        help="WordPress site root URL (default: %(default)s).",
    )
    parser.add_argument(
        "--status",
        default="draft",
        choices=["draft", "publish", "future"],
        help="WordPress post status (default: %(default)s).",
    )
    parser.add_argument(
        "--categories",
        type=int,
        nargs="*",
        help="Optional category IDs to assign to the post.",
    )
    parser.add_argument(
        "--tags",
        type=int,
        nargs="*",
        help="Optional tag IDs to assign to the post.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the upload payload without sending it to WordPress.",
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    try:
        load_env(args.env_file, overwrite=bool(args.env_file))
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc

    if args.command == "generate":
        return run_generate(args)
    if args.command == "publish":
        return run_publish(args)
    raise SystemExit("Unknown command")


def run_generate(args: argparse.Namespace) -> int:
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY or supply --api-key for article generation.")

    try:
        reference_text = fetch_reference_source(
            reference_url=args.reference_url,
            reference_file=args.reference_file,
            reference_text=args.reference_text,
        )
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Failed to load reference material: {exc}") from exc

    request = ArticleRequest(
        keyword=args.keyword,
        reference_text=reference_text,
        secondary_keywords=args.secondary_keywords,
        focus_topic=args.focus_topic,
        chart_data=args.chart_data,
        meta_title=args.meta_title,
        meta_description=args.meta_description,
        slug=args.slug,
    )

    generator = SolarArticleGenerator(
        model=args.model,
        temperature=args.temperature,
        api_key=api_key,
    )
    article_html = generator.generate(request)

    output_path = determine_output_path(args, article_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(article_html, encoding="utf-8")
    print(f"Article generated and saved to {output_path}")

    if args.username:
        args.file = str(output_path)
        return run_publish(args)

    return 0


def determine_output_path(args: argparse.Namespace, article_html: str) -> Path:
    if args.output:
        return Path(args.output)

    try:
        metadata = extract_metadata(article_html)
        slug = metadata.slug
    except (MetadataExtractionError, RuntimeError):
        slug = args.slug or args.keyword.lower().replace(" ", "-")

    return Path("content") / f"{slug}.html"


def run_publish(args: argparse.Namespace) -> int:
    password = args.password or os.getenv("WP_APPLICATION_PASSWORD")
    if not password:
        raise SystemExit("Set WP_APPLICATION_PASSWORD or supply --password for uploads.")

    if not args.file:
        raise SystemExit("--file is required when using the publish command.")

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

    result = upload_post(
        base_url=args.base_url,
        username=args.username,
        password=password,
        payload=payload,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
