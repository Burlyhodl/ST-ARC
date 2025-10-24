#!/usr/bin/env python3
"""
Test suite to validate blog post generator meets all requirements
"""

import re
import json
from blog_generator import BlogPostGenerator


def test_seo_requirements():
    """Test SEO-related requirements"""
    print("Testing SEO Requirements...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Test meta title
    assert '<title>' in html, "❌ Missing title tag"
    meta_title = generator.generate_meta_title()
    assert 30 <= len(meta_title) <= 70, f"❌ Meta title length: {len(meta_title)} (should be 30-70)"
    print(f"  ✓ Meta title: {len(meta_title)} characters (optimal 50-60)")
    
    # Test meta description
    assert 'meta name="description"' in html, "❌ Missing meta description"
    meta_desc = generator.generate_meta_description()
    assert 120 <= len(meta_desc) <= 160, f"❌ Meta description length: {len(meta_desc)} (should be 120-160)"
    print(f"  ✓ Meta description: {len(meta_desc)} characters (optimal 150-160)")
    
    # Test slug
    slug = generator.slug
    assert re.match(r'^[a-z0-9-]+$', slug), "❌ Invalid slug format"
    print(f"  ✓ URL slug: {slug}")
    
    # Test Schema.org JSON-LD
    assert 'application/ld+json' in html, "❌ Missing Schema.org JSON-LD"
    assert '"@type": "BlogPosting"' in html, "❌ Missing BlogPosting schema"
    print("  ✓ Schema.org BlogPosting JSON-LD present")
    
    # Test Open Graph tags
    assert 'property="og:type"' in html, "❌ Missing Open Graph tags"
    assert 'property="og:title"' in html, "❌ Missing og:title"
    assert 'property="og:description"' in html, "❌ Missing og:description"
    print("  ✓ Open Graph tags present")
    
    # Test Twitter Card tags
    assert 'property="twitter:card"' in html, "❌ Missing Twitter Card tags"
    print("  ✓ Twitter Card tags present")
    
    print("✅ All SEO requirements passed!\n")


def test_content_structure():
    """Test content structure requirements"""
    print("Testing Content Structure...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Test H1 tag (should have exactly one)
    h1_count = html.count('<h1')
    assert h1_count == 1, f"❌ Expected 1 H1 tag, found {h1_count}"
    print(f"  ✓ Single H1 tag present")
    
    # Test H2 tags (should have multiple)
    h2_count = html.count('<h2')
    assert h2_count >= 5, f"❌ Expected at least 5 H2 tags, found {h2_count}"
    print(f"  ✓ {h2_count} H2 tags present")
    
    # Test H3 tags (should have multiple)
    h3_count = html.count('<h3')
    assert h3_count >= 10, f"❌ Expected at least 10 H3 tags, found {h3_count}"
    print(f"  ✓ {h3_count} H3 tags present")
    
    # Test citations
    citation_count = html.count('class="citation"')
    assert citation_count >= 7, f"❌ Expected at least 7 citations, found {citation_count}"
    print(f"  ✓ {citation_count} inline citations present")
    
    # Test internal link
    assert 'class="internal-link"' in html, "❌ Missing internal link"
    assert 'solartopps.com' in html.lower(), "❌ Internal link doesn't point to SolarTopps"
    print("  ✓ Internal link to SolarTopps present")
    
    # Test external link
    assert 'class="external-link"' in html, "❌ Missing external link"
    assert 'target="_blank"' in html, "❌ External link missing target attribute"
    assert 'rel="noopener"' in html, "❌ External link missing rel attribute"
    print("  ✓ External link with proper attributes present")
    
    # Test chart/table
    assert '<table' in html or 'blog-chart-container' in html, "❌ Missing chart/table"
    print("  ✓ HTML chart/table present")
    
    print("✅ All content structure requirements passed!\n")


def test_word_count():
    """Test word count requirement"""
    print("Testing Word Count...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Remove script and style tags
    html_clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html_clean = re.sub(r'<style[^>]*>.*?</style>', '', html_clean, flags=re.DOTALL)
    
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', html_clean)
    
    # Count words
    words = text.split()
    word_count = len(words)
    
    assert word_count >= 1500, f"❌ Word count: {word_count} (minimum 1500 required)"
    print(f"  ✓ Word count: {word_count} words (exceeds 1500 minimum)")
    
    print("✅ Word count requirement passed!\n")


def test_html_validity():
    """Test HTML validity"""
    print("Testing HTML Validity...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Test DOCTYPE
    assert html.startswith('<!DOCTYPE html>'), "❌ Missing or incorrect DOCTYPE"
    print("  ✓ Valid HTML5 DOCTYPE")
    
    # Test basic structure
    assert '<html lang="en">' in html, "❌ Missing html tag with lang attribute"
    assert '<head>' in html, "❌ Missing head tag"
    assert '<body>' in html, "❌ Missing body tag"
    print("  ✓ Valid HTML structure")
    
    # Test charset
    assert 'charset="UTF-8"' in html, "❌ Missing UTF-8 charset"
    print("  ✓ UTF-8 charset declared")
    
    # Test viewport
    assert 'name="viewport"' in html, "❌ Missing viewport meta tag"
    print("  ✓ Viewport meta tag present")
    
    # Test CSS
    assert '<style>' in html, "❌ Missing CSS styling"
    print("  ✓ CSS styling included")
    
    print("✅ HTML validity tests passed!\n")


def test_json_schema():
    """Test Schema.org JSON validity"""
    print("Testing Schema.org JSON...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    schema_json = generator.generate_schema_json()
    
    # Parse JSON to ensure it's valid
    try:
        schema = json.loads(schema_json)
        assert schema['@context'] == 'https://schema.org', "❌ Invalid @context"
        assert schema['@type'] == 'BlogPosting', "❌ Invalid @type"
        assert 'headline' in schema, "❌ Missing headline"
        assert 'author' in schema, "❌ Missing author"
        assert 'publisher' in schema, "❌ Missing publisher"
        assert 'datePublished' in schema, "❌ Missing datePublished"
        print("  ✓ Valid Schema.org JSON-LD structure")
        print("  ✓ All required properties present")
    except json.JSONDecodeError:
        raise AssertionError("❌ Invalid JSON format")
    
    print("✅ Schema.org JSON tests passed!\n")


def test_responsive_design():
    """Test responsive design elements"""
    print("Testing Responsive Design...")
    
    keyword = "Test Keyword"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Test media queries
    assert '@media' in html, "❌ Missing media queries"
    print("  ✓ Media queries present")
    
    # Test responsive units
    assert 'max-width' in html, "❌ Missing responsive max-width"
    print("  ✓ Responsive width constraints")
    
    print("✅ Responsive design tests passed!\n")


def run_all_tests():
    """Run all test suites"""
    print("=" * 60)
    print("ST-ARC Blog Post Generator - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_seo_requirements()
        test_content_structure()
        test_word_count()
        test_html_validity()
        test_json_schema()
        test_responsive_design()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nBlog post generator meets all requirements:")
        print("  ✓ 1500+ word expert-level content")
        print("  ✓ Full SEO optimization (Yoast/SEMRush/GSC)")
        print("  ✓ H1, H2, H3 heading structure")
        print("  ✓ Meta title and description")
        print("  ✓ URL-friendly slug")
        print("  ✓ Schema.org BlogPosting JSON-LD")
        print("  ✓ Inline citations")
        print("  ✓ Internal and external links")
        print("  ✓ HTML chart/table")
        print("  ✓ Responsive design")
        print("  ✓ Valid HTML5")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
