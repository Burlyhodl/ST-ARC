# WordPress Upload Guide

Complete guide to uploading ST-ARC generated blog posts to WordPress.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Upload Methods](#upload-methods)
- [Configuration](#configuration)
- [Metadata Requirements](#metadata-requirements)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

## Overview

ST-ARC provides two powerful ways to upload your generated blog posts to WordPress:

1. **Standalone Upload Script** (`upload_to_wordpress.py`) - Upload existing HTML files
2. **Integrated Workflow** (`article_workflow.py`) - Generate and publish in one command

Both methods use the WordPress REST API with application password authentication.

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests>=2.31.0` - HTTP library for WordPress API calls
- `beautifulsoup4>=4.12.0` - HTML parsing (for generation)
- `lxml>=4.9.0` - XML/HTML parsing backend

### 2. Create WordPress Application Password

1. Log in to your WordPress admin dashboard
2. Navigate to **Users → Your Profile**
3. Scroll to **Application Passwords** section
4. Enter a name (e.g., "ST-ARC Uploader")
5. Click **Add New Application Password**
6. Copy the generated password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)
7. Store it securely - you won't be able to see it again

**Note:** Application passwords require WordPress 5.6+ and user accounts with publish_posts capability.

## Quick Start

### Upload Existing Article

```bash
# Set your WordPress password
export WP_APPLICATION_PASSWORD="your-app-password"

# Upload as draft
python scripts/upload_to_wordpress.py content/your-article.html \
    --username your-wordpress-username \
    --status draft

# Test first with dry-run
python scripts/upload_to_wordpress.py content/your-article.html \
    --username your-wordpress-username \
    --dry-run
```

## Upload Methods

### Method 1: Standalone Upload Script

Best for uploading pre-generated HTML files.

**Basic Usage:**
```bash
python scripts/upload_to_wordpress.py <html-file> --username <username>
```

**Full Example:**
```bash
python scripts/upload_to_wordpress.py content/solar-roi-playbook.html \
    --username admin \
    --password "xxxx xxxx xxxx xxxx xxxx xxxx" \
    --base-url https://www.solartopps.com \
    --status draft \
    --categories 5 12 \
    --tags 8 15 22
```

**Available Options:**

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `file` | Yes | Path to HTML file | - |
| `--username` | Yes | WordPress username | - |
| `--password` | No | Application password | `$WP_APPLICATION_PASSWORD` |
| `--base-url` | No | WordPress site URL | `https://www.solartopps.com` |
| `--status` | No | Post status (draft/publish/future) | `draft` |
| `--categories` | No | Category IDs (space-separated) | None |
| `--tags` | No | Tag IDs (space-separated) | None |
| `--dry-run` | No | Preview without uploading | False |

### Method 2: Integrated Workflow

Best for end-to-end generation and publishing.

**Publish Existing Article:**
```bash
python scripts/article_workflow.py publish \
    --file content/article.html \
    --username admin \
    --status publish
```

**Generate and Publish:**
```bash
export OPENAI_API_KEY="your-openai-key"
export WP_APPLICATION_PASSWORD="your-wp-password"

python scripts/article_workflow.py generate \
    "Solar Panel Efficiency 2025" \
    --reference-url https://energy.gov/solar \
    --secondary-keywords "solar efficiency" "panel performance" \
    --username admin \
    --status draft
```

**Workflow Commands:**

- `generate` - Create new article (optionally upload)
- `publish` - Upload existing article

## Configuration

### Environment Variables

Set these to avoid passing credentials on command line:

```bash
# WordPress authentication
export WP_APPLICATION_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"

# For article generation
export OPENAI_API_KEY="sk-..."

# Optional: Load from .env file
python scripts/article_workflow.py --env-file .env publish --file article.html
```

### .env File

Create a `.env` file in the project root:

```env
# WordPress Configuration
WP_APPLICATION_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_USERNAME=admin
WP_BASE_URL=https://www.solartopps.com

# OpenAI Configuration (for generation)
OPENAI_API_KEY=sk-...
```

## Metadata Requirements

Your HTML files must include these elements for upload:

### Required Metadata

```html
<head>
  <!-- Required: Title tag -->
  <title>Your Article Title Here</title>
  
  <!-- Required: Meta description -->
  <meta name="description" content="Your meta description (120-160 chars)" />
</head>
```

### Optional Metadata

```html
<body>
  <section id="meta_data">
    <!-- Optional: Custom slug -->
    <p><strong>Slug:</strong> custom-url-slug</p>
  </section>
</body>
```

**Slug Auto-Generation:**
If no slug is found, it's auto-generated from the title:
- "Solar Panel Installation 2025" → "solar-panel-installation-2025"
- Converts to lowercase
- Replaces special characters with hyphens
- Removes leading/trailing hyphens

## Examples

### Example 1: Simple Draft Upload

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username editor \
    --status draft
```

### Example 2: Publish with Categories

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --status publish \
    --categories 5 8 12
```

### Example 3: Multiple Tags

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --tags 15 22 33 44 \
    --status draft
```

### Example 4: Custom WordPress Site

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --base-url https://myblog.com \
    --password "xxxx xxxx xxxx xxxx xxxx xxxx"
```

### Example 5: Dry Run (Preview)

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --dry-run
```

Output:
```json
{
  "title": "Solar Panel Installation Guide 2025",
  "slug": "solar-panel-installation-guide-2025",
  "status": "draft",
  "content": "<html>...</html>",
  "excerpt": "Complete guide to solar panel installation in 2025."
}
```

### Example 6: Generate and Publish Workflow

```bash
python scripts/article_workflow.py generate \
    "Tesla Powerwall Cost Analysis" \
    --reference-url https://www.energy.gov/batteries \
    --secondary-keywords "battery storage" "home backup power" \
    --slug tesla-powerwall-cost \
    --username admin \
    --status draft
```

## Troubleshooting

### Authentication Error (401 Unauthorized)

**Problem:** "Upload failed with status 401"

**Solutions:**
1. Verify username is correct
2. Regenerate application password in WordPress
3. Check password doesn't have extra spaces
4. Ensure user has `publish_posts` capability
5. Verify application passwords are enabled on your WordPress site

**Test:**
```bash
curl -u username:password https://www.solartopps.com/wp-json/wp/v2/users/me
```

### Missing Metadata Error

**Problem:** "Could not find <title> tag in the HTML file"

**Solutions:**
1. Ensure HTML has `<title>` tag in `<head>`
2. Add `<meta name="description">` tag
3. Validate HTML structure

**Verify:**
```bash
grep -i "<title>" content/your-article.html
grep -i 'meta name="description"' content/your-article.html
```

### Connection Timeout

**Problem:** Upload times out

**Solutions:**
1. Check internet connection
2. Verify WordPress site URL is accessible
3. Try increasing timeout in script (default: 30s)
4. Check for firewall/proxy issues

**Test connectivity:**
```bash
curl -I https://www.solartopps.com/wp-json/wp/v2/posts
```

### Wrong Base URL

**Problem:** "Connection refused" or 404 errors

**Solutions:**
1. Verify WordPress site URL (include https://)
2. Don't include trailing slash
3. Ensure REST API is enabled

**Correct formats:**
- ✅ `https://www.solartopps.com`
- ✅ `https://myblog.com`
- ❌ `www.solartopps.com` (missing protocol)
- ❌ `https://www.solartopps.com/` (trailing slash)

### Invalid Category/Tag IDs

**Problem:** "Invalid term ID"

**Solutions:**
1. Verify category/tag IDs exist in WordPress
2. Use numeric IDs, not names
3. Check user has permission to assign categories/tags

**Get category IDs:**
```bash
curl -u username:password https://www.solartopps.com/wp-json/wp/v2/categories
```

**Get tag IDs:**
```bash
curl -u username:password https://www.solartopps.com/wp-json/wp/v2/tags
```

### Debugging

**Enable debug output:**
The scripts include debug messages to stderr. Review them for issues:

```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin 2>&1 | grep DEBUG
```

**Test with minimal payload:**
```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --dry-run | jq .
```

## API Reference

### Python Module Usage

You can use the upload functionality programmatically:

```python
from st_arc.wordpress import (
    extract_metadata,
    load_html,
    build_payload,
    upload_post,
)

# Load and parse HTML
html = load_html("content/article.html")
metadata = extract_metadata(html)

# Build WordPress payload
payload = build_payload(
    metadata,
    html,
    status="draft",
    categories=[5, 12],
    tags=[8, 15],
)

# Upload to WordPress
result = upload_post(
    base_url="https://www.solartopps.com",
    username="admin",
    password="xxxx xxxx xxxx xxxx xxxx xxxx",
    payload=payload,
    timeout=30,
)

print(f"Published! Post ID: {result['id']}")
print(f"URL: {result['link']}")
```

### Functions

**`extract_metadata(html: str) -> ArticleMetadata`**
- Extracts title, description, and slug from HTML
- Raises `MetadataExtractionError` if required fields missing

**`load_html(path: str | Path) -> str`**
- Reads HTML file from disk
- Raises `RuntimeError` on file errors

**`build_payload(metadata, content, *, status, categories, tags) -> dict`**
- Constructs WordPress API payload
- Handles optional categories and tags

**`upload_post(*, base_url, username, password, payload, timeout) -> dict`**
- Uploads post via WordPress REST API
- Returns response JSON with post ID and details
- Raises `RuntimeError` on HTTP errors

### WordPress REST API

The scripts use the WordPress REST API v2:

**Endpoint:** `POST /wp-json/wp/v2/posts`

**Authentication:** HTTP Basic Auth with application password

**Payload Format:**
```json
{
  "title": "Post Title",
  "slug": "post-slug",
  "content": "<html>...</html>",
  "excerpt": "Meta description",
  "status": "draft",
  "categories": [5, 12],
  "tags": [8, 15]
}
```

**Response:**
```json
{
  "id": 123,
  "link": "https://site.com/post-slug",
  "status": "draft",
  "title": {"rendered": "Post Title"},
  ...
}
```

## Best Practices

1. **Always test with dry-run first**
   ```bash
   --dry-run
   ```

2. **Start with draft status**
   ```bash
   --status draft
   ```

3. **Use environment variables for passwords**
   ```bash
   export WP_APPLICATION_PASSWORD="..."
   ```

4. **Validate HTML before upload**
   ```bash
   python -c "from st_arc.wordpress import extract_metadata, load_html; \
              html = load_html('article.html'); \
              print(extract_metadata(html))"
   ```

5. **Keep application passwords secure**
   - Don't commit to version control
   - Use .env files (add to .gitignore)
   - Rotate passwords regularly

6. **Monitor uploads**
   - Check WordPress admin for new posts
   - Verify metadata is correct
   - Review formatting and links

## Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review test files: `test_wordpress_upload.py`
3. Open a GitHub issue with error details
4. Include debug output from script

## Related Documentation

- [README.md](README.md) - Main project documentation
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Article generation guide
- [WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)
