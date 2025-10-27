# Quick Start Guide - SEO Blog Post Generator

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Interactive Mode

```bash
python seo_blog_generator.py
```

Follow the prompts to:
1. Choose input method (URL, text, or file)
2. Enter target keyword
3. Add optional secondary keywords
4. Specify custom slug (or auto-generate)
5. Add custom data for visualization (optional)

### Programmatic Usage

```python
from seo_blog_generator import SEOBlogGenerator

# Initialize generator
generator = SEOBlogGenerator()

# Generate blog post
result = generator.generate_wordpress_html(
    input_content="Your reference content here",
    keyword="your target keyword",
    secondary_keywords=["keyword1", "keyword2"],  # optional
    custom_slug="custom-url-slug",  # optional
    data_points={  # optional
        'labels': ['2020', '2021', '2022', '2023'],
        'values': [10, 25, 45, 70],
        'title': 'Growth Over Time'
    }
)

# Access results
print(result['title'])
print(result['slug'])
print(result['meta_description'])
print(result['word_count'])
print(result['content'])  # WordPress-ready HTML
```

## Output Structure

The generator returns:

```python
{
    'title': 'SEO-optimized title with keyword',
    'slug': 'url-friendly-slug',
    'meta_description': '155-160 character description',
    'schema': 'JSON-LD BlogPosting schema',
    'content': 'WordPress-ready HTML content',
    'links': [
        {
            'url': 'https://example.com',
            'anchor_text': 'descriptive link text',
            'purpose': 'External authority link'
        }
    ],
    'word_count': 1526
}
```

## WordPress Integration

### Copy-Paste Method (Easiest)

1. Run the generator
2. Copy the output HTML
3. In WordPress, create new post
4. Switch to "Code Editor" mode
5. Paste the HTML
6. Set title, slug, and meta description
7. Publish or save draft

### REST API Method (Advanced)

```python
import requests

wp_url = "https://solartopps.com/wp-json/wp/v2/posts"
wp_user = "username"
wp_password = "app_password"

result = generator.generate_wordpress_html(...)

response = requests.post(
    wp_url,
    json={
        'title': result['title'],
        'content': result['content'],
        'slug': result['slug'],
        'status': 'draft'
    },
    auth=(wp_user, wp_password)
)
```

## SEO Checklist

The generator automatically ensures:

✅ **Keyword Optimization**
- Keyword in title
- Keyword in meta description
- Keyword in first paragraph
- Keyword in H2 heading
- 5+ keyword instances throughout

✅ **Content Quality**
- 1500+ words
- Multiple H2 and H3 headings
- Short paragraphs (2-5 lines)
- Bullet points and lists
- Active voice (>90%)
- Transition words (>30%)

✅ **Technical SEO**
- Proper HTML5 structure
- JSON-LD BlogPosting schema
- Meta description (155-160 chars)
- SEO-friendly slug
- Canonical URL

✅ **User Experience**
- Montserrat font
- Clean formatting
- Data visualization
- External authority links
- Mobile-responsive

## Examples

See `example_usage.py` for complete examples:

```bash
python example_usage.py
```

## Testing

Run the test suite:

```bash
python -m unittest test_seo_blog_generator.py -v
```

## Troubleshooting

### URL Not Loading
- Check internet connection
- Verify URL is accessible
- Try using text input instead

### Low Word Count
- Provide more detailed reference content
- Template automatically generates 1500+ words

### Keyword Not Appearing
- Check keyword spelling
- Keywords are automatically integrated 5+ times

## Tips for Best Results

1. **Keywords**: Use specific, realistic keywords
   - Good: "Tesla Powerwall installation cost Arizona"
   - Bad: "solar" (too broad)

2. **Reference Content**: Provide quality sources
   - Use trusted sources
   - Include relevant statistics
   - Ensure factual accuracy

3. **Citations**: Generator auto-links to:
   - .gov sites (e.g., energy.gov)
   - .edu sites (e.g., research labs)
   - Industry authorities (e.g., SEIA)

4. **Data Visualization**: Best with 4-6 data points
   - Use relevant metrics
   - Keep labels short
   - Values should be numeric

## Support

For issues or questions:
- Check the full README.md
- Review example_usage.py
- Run tests to verify setup

## Credits

For more GPTs by God of Prompt, visit https://godofprompt.ai/gpts
