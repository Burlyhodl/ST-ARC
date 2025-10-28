#!/usr/bin/env python3
"""Unit tests for WordPress upload functionality."""

import unittest
from unittest.mock import MagicMock, patch

from st_arc.wordpress import (
    ArticleMetadata,
    MetadataExtractionError,
    build_payload,
    clean_html_whitespace,
    extract_metadata,
    load_html,
    slugify,
    upload_post,
)


class TestMetadataExtraction(unittest.TestCase):
    """Test metadata extraction from HTML articles."""

    def test_extract_valid_metadata(self):
        """Test extraction of all metadata from valid HTML."""
        html = """
        <html>
        <head>
            <title>Solar Panel Installation Guide</title>
            <meta name="description" content="Complete guide to solar panel installation in 2025." />
        </head>
        <body>
            <p><strong>Slug:</strong> solar-panel-installation-guide</p>
        </body>
        </html>
        """
        metadata = extract_metadata(html)
        self.assertEqual(metadata.title, "Solar Panel Installation Guide")
        self.assertEqual(metadata.description, "Complete guide to solar panel installation in 2025.")
        self.assertEqual(metadata.slug, "solar-panel-installation-guide")

    def test_extract_metadata_without_slug(self):
        """Test that slug is auto-generated when not present."""
        html = """
        <html>
        <head>
            <title>Solar Battery Storage</title>
            <meta name="description" content="Learn about solar battery storage options." />
        </head>
        </html>
        """
        metadata = extract_metadata(html)
        self.assertEqual(metadata.title, "Solar Battery Storage")
        self.assertEqual(metadata.slug, "solar-battery-storage")

    def test_extract_metadata_missing_title(self):
        """Test error when title is missing."""
        html = """
        <html>
        <head>
            <meta name="description" content="Description only." />
        </head>
        </html>
        """
        with self.assertRaises(MetadataExtractionError) as ctx:
            extract_metadata(html)
        self.assertIn("title", str(ctx.exception).lower())

    def test_extract_metadata_missing_description(self):
        """Test error when description is missing."""
        html = """
        <html>
        <head>
            <title>Test Title</title>
        </head>
        </html>
        """
        with self.assertRaises(MetadataExtractionError) as ctx:
            extract_metadata(html)
        self.assertIn("description", str(ctx.exception).lower())

    def test_clean_html_whitespace(self):
        """Test whitespace cleaning utility."""
        dirty = "  Multiple   spaces\n\tand\ttabs  "
        clean = clean_html_whitespace(dirty)
        self.assertEqual(clean, "Multiple spaces and tabs")

    def test_metadata_whitespace_cleanup(self):
        """Test that extracted metadata has whitespace cleaned."""
        html = """
        <html>
        <head>
            <title>  Title with
            extra   whitespace  </title>
            <meta name="description" content="Description  with    spaces" />
        </head>
        </html>
        """
        metadata = extract_metadata(html)
        self.assertEqual(metadata.title, "Title with extra whitespace")
        self.assertEqual(metadata.description, "Description with spaces")


class TestSlugify(unittest.TestCase):
    """Test slug generation functionality."""

    def test_slugify_basic(self):
        """Test basic slugification."""
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_special_characters(self):
        """Test slugification removes special characters."""
        self.assertEqual(slugify("Solar Panel's Cost: $15,000!"), "solar-panel-s-cost-15-000")

    def test_slugify_multiple_separators(self):
        """Test slugification handles multiple separators."""
        self.assertEqual(slugify("Test---Multiple---Dashes"), "test-multiple-dashes")

    def test_slugify_leading_trailing_dashes(self):
        """Test slugification removes leading/trailing dashes."""
        self.assertEqual(slugify("---Test Slug---"), "test-slug")


class TestPayloadBuilding(unittest.TestCase):
    """Test WordPress payload construction."""

    def test_build_basic_payload(self):
        """Test building a basic payload."""
        metadata = ArticleMetadata(
            title="Test Article",
            description="Test description",
            slug="test-article",
        )
        content = "<p>Test content</p>"
        
        payload = build_payload(metadata, content, status="draft")
        
        self.assertEqual(payload["title"], "Test Article")
        self.assertEqual(payload["slug"], "test-article")
        self.assertEqual(payload["status"], "draft")
        self.assertEqual(payload["content"], "<p>Test content</p>")
        self.assertEqual(payload["excerpt"], "Test description")

    def test_build_payload_with_categories(self):
        """Test payload includes categories."""
        metadata = ArticleMetadata(
            title="Test",
            description="Desc",
            slug="test",
        )
        payload = build_payload(
            metadata,
            "content",
            status="publish",
            categories=[1, 2, 3],
        )
        self.assertEqual(payload["categories"], [1, 2, 3])

    def test_build_payload_with_tags(self):
        """Test payload includes tags."""
        metadata = ArticleMetadata(
            title="Test",
            description="Desc",
            slug="test",
        )
        payload = build_payload(
            metadata,
            "content",
            status="future",
            tags=[10, 20],
        )
        self.assertEqual(payload["tags"], [10, 20])

    def test_build_payload_without_optional_fields(self):
        """Test payload without categories or tags."""
        metadata = ArticleMetadata(
            title="Test",
            description="Desc",
            slug="test",
        )
        payload = build_payload(metadata, "content", status="draft")
        self.assertNotIn("categories", payload)
        self.assertNotIn("tags", payload)


class TestLoadHtml(unittest.TestCase):
    """Test HTML file loading."""

    @patch("pathlib.Path.read_text")
    def test_load_html_success(self, mock_read):
        """Test successful HTML loading."""
        mock_read.return_value = "<html>Test</html>"
        result = load_html("test.html")
        self.assertEqual(result, "<html>Test</html>")
        mock_read.assert_called_once_with(encoding="utf-8")

    @patch("pathlib.Path.read_text")
    def test_load_html_error(self, mock_read):
        """Test HTML loading error handling."""
        mock_read.side_effect = OSError("File not found")
        with self.assertRaises(RuntimeError) as ctx:
            load_html("missing.html")
        self.assertIn("Failed to read", str(ctx.exception))


class TestUploadPost(unittest.TestCase):
    """Test WordPress post upload functionality."""

    @patch("requests.post")
    def test_upload_success(self, mock_post):
        """Test successful post upload."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 123, "status": "draft"}
        mock_post.return_value = mock_response

        payload = {"title": "Test", "content": "Content"}
        result = upload_post(
            base_url="https://example.com",
            username="testuser",
            password="testpass",
            payload=payload,
        )

        self.assertEqual(result, {"id": 123, "status": "draft"})
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args.kwargs["auth"], ("testuser", "testpass"))
        self.assertIn("wp-json/wp/v2/posts", call_args.args[0])

    @patch("requests.post")
    def test_upload_error(self, mock_post):
        """Test upload error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        payload = {"title": "Test"}
        with self.assertRaises(RuntimeError) as ctx:
            upload_post(
                base_url="https://example.com",
                username="baduser",
                password="badpass",
                payload=payload,
            )
        self.assertIn("401", str(ctx.exception))
        self.assertIn("Unauthorized", str(ctx.exception))

    @patch("requests.post")
    def test_upload_timeout_parameter(self, mock_post):
        """Test that timeout parameter is passed correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        upload_post(
            base_url="https://example.com",
            username="user",
            password="pass",
            payload={},
            timeout=60,
        )

        call_args = mock_post.call_args
        self.assertEqual(call_args.kwargs["timeout"], 60)


if __name__ == "__main__":
    unittest.main()
