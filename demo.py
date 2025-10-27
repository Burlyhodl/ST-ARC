#!/usr/bin/env python3
"""
Demonstration of ST-ARC Blog Post Generator
Shows all features and capabilities
"""

import os
from blog_generator import BlogPostGenerator


def demo_basic_usage():
    """Demonstrate basic usage"""
    print("=" * 70)
    print("DEMO 1: Basic Usage with Placeholder")
    print("=" * 70)
    
    keyword = "[KEYWORD]"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    filename = "demo_placeholder.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {filename}")
    print(f"  - Keyword: {keyword}")
    print(f"  - Slug: {generator.slug}")
    print(f"  - File size: {len(html)} bytes")
    print(f"  - Word count: {len(html.split())} words")
    print()


def demo_real_keyword():
    """Demonstrate with real solar energy keyword"""
    print("=" * 70)
    print("DEMO 2: Real Solar Energy Keyword")
    print("=" * 70)
    
    keyword = "Residential Solar Battery Storage Systems"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    filename = f"demo_{generator.slug}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {filename}")
    print(f"  - Keyword: {keyword}")
    print(f"  - Slug: {generator.slug}")
    print(f"  - Meta Title: {generator.generate_meta_title()}")
    print(f"  - Meta Description: {generator.generate_meta_description()[:60]}...")
    print(f"  - URL: https://www.solartopps.com/blog/{generator.slug}/")
    print()


def demo_metadata_access():
    """Demonstrate accessing individual components"""
    print("=" * 70)
    print("DEMO 3: Accessing Individual Components")
    print("=" * 70)
    
    keyword = "Net Metering and Solar Credits"
    generator = BlogPostGenerator(keyword)
    
    print(f"Keyword: {keyword}")
    print(f"Slug: {generator.slug}")
    print(f"Meta Title: {generator.generate_meta_title()}")
    print(f"Meta Description: {generator.generate_meta_description()}")
    print(f"Publication Date: {generator.date_published}")
    print()
    print("Schema.org JSON (first 200 chars):")
    print(generator.generate_schema_json()[:200] + "...")
    print()


def demo_multiple_keywords():
    """Demonstrate generating multiple blog posts"""
    print("=" * 70)
    print("DEMO 4: Batch Generation (Multiple Keywords)")
    print("=" * 70)
    
    keywords = [
        "Solar Panel Cleaning and Maintenance",
        "Off-Grid Solar Power Systems",
        "Commercial Solar ROI Calculator"
    ]
    
    for i, keyword in enumerate(keywords, 1):
        generator = BlogPostGenerator(keyword)
        html = generator.generate_full_html()
        
        filename = f"demo_batch_{i}_{generator.slug}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ [{i}/3] Generated: {filename}")
        print(f"        Slug: {generator.slug}")
    
    print()


def demo_statistics():
    """Show statistics about generated content"""
    print("=" * 70)
    print("DEMO 5: Content Statistics")
    print("=" * 70)
    
    keyword = "Solar Panel Efficiency Ratings"
    generator = BlogPostGenerator(keyword)
    html = generator.generate_full_html()
    
    # Count elements
    h1_count = html.count('<h1')
    h2_count = html.count('<h2')
    h3_count = html.count('<h3')
    citation_count = html.count('class="citation"')
    has_internal_link = 'class="internal-link"' in html
    has_external_link = 'class="external-link"' in html
    has_chart = '<table' in html or 'blog-chart-container' in html
    has_schema = 'application/ld+json' in html
    
    print(f"Content Analysis for: {keyword}")
    print(f"  - H1 headings: {h1_count}")
    print(f"  - H2 headings: {h2_count}")
    print(f"  - H3 headings: {h3_count}")
    print(f"  - Citations: {citation_count}")
    print(f"  - Internal link: {'✓' if has_internal_link else '✗'}")
    print(f"  - External link: {'✓' if has_external_link else '✗'}")
    print(f"  - Chart/Table: {'✓' if has_chart else '✗'}")
    print(f"  - Schema.org: {'✓' if has_schema else '✗'}")
    print(f"  - File size: {len(html):,} bytes")
    print()


def cleanup_demo_files():
    """Clean up demo files"""
    print("=" * 70)
    print("Cleanup")
    print("=" * 70)
    
    demo_files = [f for f in os.listdir('.') if f.startswith('demo_')]
    
    if demo_files:
        response = input(f"Delete {len(demo_files)} demo files? (y/n): ")
        if response.lower() == 'y':
            for f in demo_files:
                os.remove(f)
                print(f"  Deleted: {f}")
            print(f"✓ Cleaned up {len(demo_files)} files")
        else:
            print("✓ Demo files kept")
    else:
        print("No demo files to clean up")
    print()


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "ST-ARC BLOG POST GENERATOR DEMO" + " " * 21 + "║")
    print("║" + " " * 20 + "SolarTopps.com Edition" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    try:
        demo_basic_usage()
        demo_real_keyword()
        demo_metadata_access()
        demo_multiple_keywords()
        demo_statistics()
        
        print("=" * 70)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("Generated files:")
        demo_files = [f for f in os.listdir('.') if f.startswith('demo_')]
        for f in demo_files:
            size = os.path.getsize(f)
            print(f"  - {f} ({size:,} bytes)")
        print()
        
        cleanup_demo_files()
        
        print("=" * 70)
        print("Next Steps:")
        print("  1. Open any demo_*.html file in a browser")
        print("  2. Review the generated content")
        print("  3. Use blog_generator.py to create your own")
        print("  4. Run test_blog_generator.py to validate")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        raise


if __name__ == "__main__":
    main()
