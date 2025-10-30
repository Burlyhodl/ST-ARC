#!/usr/bin/env python3
"""
SEO Blog Generator adapter + standalone generator for SolarTopps.

- When imported by app.py this module provides SEOBlogGenerator with:
    - fetch_url_content(url) -> str
    - generate_wordpress_html(input_content, keyword, secondary_keywords=None, custom_slug=None, data_points=None) -> dict
      (returns at minimum: html, slug, meta_title, meta_description)

- When executed as a script (python seo_blog_generator.py) it runs a simple interactive CLI using
  the same SEOBlogGenerator class.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

# Note: do not exit at import-time if requests/bs4 are missing. Let runtime calls raise clear errors.

class SEOBlogGenerator:
    """Comprehensive SEO blog generator that also acts as an adapter for app.py."""

    def __init__(self, user_agent: str = "st-arc-bot/1.0"):
        self.headers = {"User-Agent": user_agent}
        # default generation parameters
        self.word_count_target = 1500

    #
    # Content fetching utilities
    #
    def fetch_url_content(self, url: str) -> str:
        """Fetch page and return main text.

        Tries semantic containers first (<article>, <main>), then common selectors,
        then body, then whole page text. Returns empty string on failure.
        """
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            # Prefer semantic containers
            article = soup.find("article")
            if article and article.get_text(strip=True):
                return article.get_text(separator="\n", strip=True)

            main = soup.find("main")
            if main and main.get_text(strip=True):
                return main.get_text(separator="\n", strip=True)

            # Try common content containers
            selectors = [".post-content", ".article-body", ".content", ".entry-content"]
            for sel in selectors:
                node = soup.select_one(sel)
                if node and node.get_text(strip=True):
                    return node.get_text(separator="\n", strip=True)

            if soup.body and soup.body.get_text(strip=True):
                return soup.body.get_text(separator="\n", strip=True)

            # Fallback: whole page text
            return soup.get_text(separator="\n", strip=True)

        except Exception:
            # Don't print or exit during import; return empty content so caller can handle it
            return ""

    def load_file_content(self, filepath: str) -> str:
        """Load content from a local file (used by CLI)."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    #
    # Metadata / helper generators
    #
    def generate_slug(self, title: str) -> str:
        slug = title.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    def generate_meta_description(self, keyword: str, content_snippet: str) -> str:
        description = f"Discover {keyword} insights and expert analysis. {content_snippet}"
        if len(description) < 120:
            description += " Learn from industry experts at SolarTopps."
        if len(description) > 160:
            description = description[:157] + "..."
        return description

    def generate_title(self, keyword: str) -> str:
        templates = [
            f"Complete Guide to {keyword.title()} | SolarTopps",
            f"{keyword.title()}: Expert Analysis and Insights",
            f"Understanding {keyword.title()} - Professional Guide",
            f"{keyword.title()}: Everything You Need to Know",
        ]
        return templates[0] if len(keyword) < 30 else templates[1]

    def generate_json_ld_schema(self, title: str, description: str, date_published: str, slug: str) -> str:
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": description,
            "author": {"@type": "Organization", "name": "SolarTopps"},
            "publisher": {
                "@type": "Organization",
                "name": "SolarTopps",
                "logo": {"@type": "ImageObject", "url": "https://solartopps.com/logo.png"},
            },
            "datePublished": date_published,
            "dateModified": date_published,
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://solartopps.com/blog/{slug}"},
            "image": f"https://solartopps.com/blog/images/{slug}.jpg",
        }
        return json.dumps(schema, indent=2)

    #
    # Data visualization placeholder
    #
    def generate_data_visualization(self, data_points: Optional[Dict] = None) -> str:
        if not data_points:
            data_points = {"labels": ["2020", "2021", "2022", "2023", "2024"], "values": [15, 23, 35, 48, 62], "title": "Solar Installation Growth (%)"}
        chart_html = f"""
<div class="data-visualization" style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
    <h3 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-bottom: 15px;">{data_points['title']}</h3>
    <canvas id="dataChart" style="max-width: 100%; height: 300px;"></canvas>
</div>
<script>
(function() {{
    const canvas = document.getElementById('dataChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const labels = {json.dumps(data_points['labels'])};
    const values = {json.dumps(data_points['values'])};
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 300;
    const padding = 40;
    const barWidth = (width - padding * 2) / labels.length * 0.8;
    const maxValue = Math.max(...values || [1]);
    ctx.fillStyle = '#3498db';
    values.forEach((value, i) => {{
        const barHeight = (value / maxValue) * (height - padding * 2);
        const x = padding + i * (width - padding * 2) / labels.length + barWidth * 0.1;
        const y = height - padding - barHeight;
        ctx.fillRect(x, y, barWidth, barHeight);
        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Montserrat, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(value + '%', x + barWidth / 2, y - 5);
        ctx.fillText(labels[i], x + barWidth / 2, height - padding + 20);
        ctx.fillStyle = '#3498db';
    }});
}})();
</script>
"""
        return chart_html

    #
    # Content generator (HTML)
    #
    def generate_html_content(self, title: str, keyword: str, secondary_keywords: List[str], reference_content: str) -> str:
        """Build article body. This is the same structure used previously (templated paragraphs)."""
        paragraphs = []

        intro = f"""<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
In today's rapidly evolving energy landscape, understanding <strong>{keyword}</strong> is crucial for homeowners and businesses alike. 
This comprehensive guide explores the key aspects of {keyword}, providing expert insights backed by industry research and real-world data. 
Whether you're considering solar energy for the first time or looking to optimize your existing system, this article will equip you with 
the knowledge you need to make informed decisions.
</p>"""
        paragraphs.append(intro)

        # Add several sections (kept concise here, same as your original version)
        sections = [
            ("Understanding {k}: The Fundamentals", f"When it comes to {keyword}, many homeowners feel overwhelmed by technical jargon..."),
            ("Key Benefits of {k}", "The advantages extend beyond cost savings: energy independence, environmental impact, financial returns..."),
            ("Technical Aspects and Performance Metrics", "Understanding technical specifications helps you make informed decisions..."),
            ("Financial Considerations and ROI", "Initial investment may be large but incentives and savings can yield favorable ROI..."),
            ("Installation Process Explained", "From site assessment to interconnection, the process usually takes several weeks..."),
            ("Maintenance Requirements and Long-Term Performance", "Panels require minimal maintenance; most have 25-year warranties..."),
            ("Selecting the Right System for Your Needs", "Consider consumption patterns, roof characteristics, and budget...")
        ]

        for heading, body in sections:
            paragraphs.append(f"<h2 style=\"font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;\">{heading.format(k=keyword)}</h2>")
            paragraphs.append(f"<p style=\"font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;\">{body}</p>")

        # Append conclusion and reference content (if provided)
        conclusion = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">Conclusion: Embracing the Solar Future</h2>
<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
As we've explored throughout this guide, {keyword} represents more than just a trend—it's a fundamental shift in how we generate and consume energy...
</p>"""
        paragraphs.append(conclusion)

        if reference_content:
            # escape minimally and include
            snippet = self._escape_html_snippet(reference_content)
            ref_html = f"""<section><h2>Source / Reference Content</h2><div class="source-content" style="white-space:pre-wrap; background:#f4f4f4; padding:12px; border-radius:6px;">{snippet}</div></section>"""
            paragraphs.insert(1, ref_html)

        return "\n\n".join(paragraphs)

    def generate_complete_html(self, input_content: str, keyword: str, secondary_keywords: Optional[List[str]] = None, custom_slug: str = None, data_points: Dict = None) -> str:
        """Generate a full standalone HTML page (complete head/body)."""
        if secondary_keywords is None:
            secondary_keywords = []
        title = self.generate_title(keyword)
        slug = custom_slug if custom_slug else self.generate_slug(title)
        meta_description = self.generate_meta_description(keyword, "Learn about solar energy solutions, installation processes, and cost considerations from industry experts.")
        date_published = datetime.now().isoformat()
        schema = self.generate_json_ld_schema(title, meta_description, date_published, slug)
        content = self.generate_html_content(title, keyword, secondary_keywords, input_content)
        visualization = self.generate_data_visualization(data_points)
        complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="https://solartopps.com/blog/{slug}">
  <script type="application/ld+json">{schema}</script>
  <style>/* minimal inline styles omitted for brevity in this view */</style>
</head>
<body>
  <article>
    <header><h1>{title}</h1></header>
    {content}
    {visualization}
  </article>
</body>
</html>"""
        return complete_html

    def generate_wordpress_html(self, input_content: str, keyword: str, secondary_keywords: Optional[List[str]] = None, custom_slug: Optional[str] = None, data_points: Optional[Dict] = None) -> Dict:
        """Adapter method expected by app.py.

        Returns at minimum:
            - html: full HTML (complete page)
            - slug
            - meta_title
            - meta_description

        Additionally returns:
            - content: WordPress-ready body (HTML snippet)
            - schema
            - links
            - word_count
        """
        if secondary_keywords is None:
            secondary_keywords = []

        title = self.generate_title(keyword)
        slug = custom_slug if custom_slug else self.generate_slug(title)
        meta_description = self.generate_meta_description(keyword, "Learn about solar energy solutions from industry experts at SolarTopps.")
        date_published = datetime.now().isoformat()
        schema = self.generate_json_ld_schema(title, meta_description, date_published, slug)
        content = self.generate_html_content(title, keyword, secondary_keywords, input_content)
        visualization = self.generate_data_visualization(data_points)
        wordpress_content = f"""<div style="font-family: Montserrat, sans-serif;">
  <h1>{title}</h1>
  {content}
  {visualization}
</div>
<script type="application/ld+json">{schema}</script>"""

        # extract links
        links = []
        link_pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        for match in re.finditer(link_pattern, wordpress_content):
            links.append({"url": match.group(1), "anchor_text": match.group(2), "purpose": "External authority link"})

        result = {
            "html": self.generate_complete_html(input_content, keyword, secondary_keywords, custom_slug, data_points),
            "slug": slug,
            "meta_title": title,
            "meta_description": meta_description,
            "content": wordpress_content,
            "schema": schema,
            "links": links,
            "word_count": len(re.sub(r"<[^>]+>", " ", wordpress_content).split()),
        }
        return result

    def _escape_html_snippet(self, text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

#
# CLI section (runs only when executed directly)
#
def _run_cli():
#    import sys
#    gen = SEOBlogGenerator()
#    print("=" * 80)
#    print("Automated SEO Blog Post Generator for SolarTopps")
#    print("=" * 80)
#    print()
#    print("1) Enter URL  2) Paste text  3) Load from file")
#    choice = input("Select input method (1-3): ").strip()
#    input_content = ""
#    if choice == "1":
#        url = input("URL: ").strip()
#        input_content = gen.fetch_url_content(url) or ""
#    elif choice == "2":
#        print("Paste content, then press Ctrl-D / Ctrl-Z:")
#        input_content = sys.stdin.read()
#    elif choice == "3":
#        path = input("File path: ").strip()
#        input_content = gen.load_file_content(path) or ""
#    else:
#        input_content = ""

#    keyword = input("Enter keyword/phrase: ").strip()
#    if not keyword:
#        print("Keyword required; exiting.")
#        return

#    secondary = input("Secondary keywords (comma-separated, optional): ").strip()
#    secondary_keywords = [k.strip() for k in secondary.split(",")] if secondary else []
#    slug = input("Preferred slug (optional): ").strip() or None
#    use_data = input("Provide custom data for visualization? (y/n): ").strip().lower() == "y"
#    data_points = None
#    if use_data:
#        raw = input("Enter label:value pairs (label1:val1,label2:val2,...): ").strip()
#        try:
#            labels, values = [], []
#            for p in raw.split(","):
#                l, v = p.split(":")
#                labels.append(l.strip())
#                values.append(float(v.strip()))
#            data_points = {"labels": labels, "values": values, "title": f"{keyword} - Metrics"}
#        except Exception:
#            data_points = None

#    result = gen.generate_wordpress_html(input_content, keyword, secondary_keywords, slug, data_points)
#    # Print summary
#    print("\n[RESULT]")
#    print("Title:", result.get("meta_title"))
#    print("Slug:", result.get("slug"))
#    print("Meta Desc:", result.get("meta_description"))
#    print("Word count (approx):", result.get("word_count"))
#    out_file = f"blog_{result.get('slug', 'output')}.html"
#    with open(out_file, "w", encoding="utf-8") as f:
#        f.write(result.get("content", result.get("html", "")))
#    print("Saved to", out_file)

if __name__ == "__main__":
    _run_cli()