#!/usr/bin/env python3
"""
Example: Generate a blog post with a real keyword
"""

from blog_generator import BlogPostGenerator

# Example with a real solar energy keyword
keyword = "Solar Panel Installation Cost 2025"

# Create the generator
generator = BlogPostGenerator(keyword)

# Generate the HTML
html_content = generator.generate_full_html()

# Save to file
output_file = f"example_{generator.slug}.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Generated example blog post: {output_file}")
print(f"✓ Keyword: {keyword}")
print(f"✓ Slug: {generator.slug}")
print(f"✓ Meta Title: {generator.generate_meta_title()}")
print(f"✓ Meta Description: {generator.generate_meta_description()}")
print(f"✓ URL: https://www.solartopps.com/blog/{generator.slug}/")
print(f"\nOpen {output_file} in your browser to preview!")
