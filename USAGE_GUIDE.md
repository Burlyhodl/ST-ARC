# Quick Start Guide

## Overview
The ST-ARC Blog Post Generator creates professional, SEO-optimized HTML blog posts for SolarTopps.com with 1500+ words of expert-level content.

## Installation
No installation required! Just Python 3.6+

```bash
# Clone the repository
git clone https://github.com/Burlyhodl/ST-ARC.git
cd ST-ARC

# Verify Python version
python3 --version
```

## Basic Usage

### Option 1: Generate with Placeholder Keyword

```bash
python3 blog_generator.py
```

This creates:
- `blog_post_keyword.html` - Complete blog post with `[KEYWORD]` placeholder
- `blog_post_keyword_metadata.json` - Metadata file

**Then:** Replace `[KEYWORD]` throughout the HTML with your actual keyword.

### Option 2: Generate with Specific Keyword

```bash
python3 example_usage.py
```

Or create your own script:

```python
from blog_generator import BlogPostGenerator

# Your keyword here
keyword = "Solar Panel Efficiency in Cold Climates"

# Generate
generator = BlogPostGenerator(keyword)
html = generator.generate_full_html()

# Save
with open(f"{generator.slug}.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated: {generator.slug}.html")
```

## What You Get

### 1. Complete HTML File
- 1500+ words of expert content
- Full SEO optimization
- Responsive design
- Professional styling

### 2. Metadata JSON File
```json
{
  "keyword": "Your Keyword",
  "slug": "your-keyword",
  "meta_title": "Your Keyword | Complete Expert Guide 2025",
  "meta_description": "Expert guide to Your Keyword...",
  "date_published": "2025-10-24",
  "url": "https://www.solartopps.com/blog/your-keyword/"
}
```

## Testing

Run the comprehensive test suite:

```bash
python3 test_blog_generator.py
```

This validates:
- ✅ SEO requirements (meta tags, schema, etc.)
- ✅ Content structure (headings, links, citations)
- ✅ Word count (1500+ words)
- ✅ HTML validity
- ✅ Schema.org JSON
- ✅ Responsive design

## Customization

### Change Internal Link

Edit `blog_generator.py` line ~257:

```python
<a href="https://www.solartopps.com/YOUR-PAGE/" class="internal-link">
```

### Change External Link

Edit `blog_generator.py` line ~332:

```python
<a href="https://YOUR-AUTHORITATIVE-SOURCE.com" class="external-link">
```

### Modify Colors

Edit the `<style>` section in `blog_generator.py`:

```python
# Primary accent color
border-bottom: 3px solid #ff6b35;  # Change #ff6b35 to your color

# Text color
color: #2c3e50;  # Change #2c3e50 to your color
```

### Customize Chart Data

Edit the `generate_chart_html()` method in `blog_generator.py` to modify the table data.

## Publishing to WordPress/CMS

### Option 1: Copy HTML Content
1. Open the generated HTML file
2. Copy everything inside `<article>` tags
3. Paste into WordPress HTML editor

### Option 2: Import via Custom Field
1. Copy the entire HTML
2. Use a plugin like "Advanced Custom Fields"
3. Create a custom HTML field
4. Paste the content

### Option 3: Convert to WordPress Format
1. Extract the `<style>` section
2. Add to your theme's CSS
3. Copy the body content
4. Add custom fields for schema.org JSON

## SEO Optimization Checklist

After generating your blog post:

- [ ] Replace `[KEYWORD]` with actual keyword (if using placeholder method)
- [ ] Review and adjust meta title (aim for 50-60 characters)
- [ ] Review and adjust meta description (aim for 150-160 characters)
- [ ] Update the featured image path
- [ ] Verify internal link points to correct page
- [ ] Verify external link is authoritative
- [ ] Customize chart data for your specific keyword
- [ ] Add actual statistics and citations
- [ ] Review content for keyword density (aim for 1-2%)
- [ ] Check readability score (aim for Flesch Reading Ease 50-70)

## Troubleshooting

### "Command not found: python3"
- Try `python` instead of `python3`
- Or install Python 3: https://www.python.org/downloads/

### "No module named 'blog_generator'"
- Make sure you're in the correct directory
- Run `python3 blog_generator.py` (not `python3 -m blog_generator`)

### Word count seems low
- The generator includes 1600+ words of text content
- HTML tags are not counted in the word count
- Run `test_blog_generator.py` to verify

## Examples

### Example 1: Solar Panel Topic
```python
keyword = "Best Solar Panels for Home Use 2025"
generator = BlogPostGenerator(keyword)
html = generator.generate_full_html()
# Generates: blog post about best solar panels
```

### Example 2: Energy Storage
```python
keyword = "Lithium Iron Phosphate Battery Storage"
generator = BlogPostGenerator(keyword)
html = generator.generate_full_html()
# Generates: blog post about LiFePO4 batteries
```

### Example 3: Solar Incentives
```python
keyword = "Federal Solar Tax Credit ITC 2025"
generator = BlogPostGenerator(keyword)
html = generator.generate_full_html()
# Generates: blog post about solar tax credits
```

## Best Practices

1. **Keyword Research**: Use tools like Google Keyword Planner before generating
2. **Fact Checking**: Replace placeholder data with accurate statistics
3. **Citation Updates**: Add links to real sources in the citations section
4. **Image Optimization**: Add actual images and optimize alt text
5. **Internal Linking**: Update internal links to actual related articles
6. **Regular Updates**: Update date_modified when making changes
7. **Mobile Testing**: Always test on mobile devices
8. **Page Speed**: Optimize images and consider lazy loading

## Support

For issues or questions:
1. Check this guide
2. Run `test_blog_generator.py` to diagnose issues
3. Open a GitHub issue with details

## License

This tool is designed for SolarTopps.com content creation.

---

**Generated by ST-ARC** - Professional blog content generation
