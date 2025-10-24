# ST-ARC
ST-Article Creator and AI article generator 

## 🚀 SolarTopps Blog Post Generator

A professional-grade HTML blog post generator specifically designed for SolarTopps.com. This tool creates fully SEO-optimized, expert-level blog posts with comprehensive features including structured data, citations, and responsive design.

## ✨ Features

### SEO Optimization
- ✅ **Meta Title** (optimal 50-60 characters, acceptable 30-70)
- ✅ **Meta Description** (optimal 150-160 characters, acceptable 120-160)
- ✅ **URL-Friendly Slug** (automatically generated from keyword)
- ✅ **Schema.org BlogPosting JSON-LD** (structured data for search engines)
- ✅ **Open Graph Tags** (Facebook/social media optimization)
- ✅ **Twitter Card Tags** (Twitter sharing optimization)
- ✅ **Semantic HTML5** (proper heading hierarchy)

### Content Structure
- ✅ **H1, H2, H3 Headings** (proper hierarchical structure)
- ✅ **1500+ Words** (expert-level, comprehensive content)
- ✅ **Inline Citations** (7 academic-style references)
- ✅ **1 Internal Link** (to SolarTopps.com pages)
- ✅ **1 External Link** (to authoritative sources like energy.gov)
- ✅ **HTML Chart/Table** (data visualization with comparison metrics)

### Professional Design
- ✅ **Responsive CSS** (mobile-friendly, modern design)
- ✅ **Color Scheme** (matching SolarTopps brand - #ff6b35 accent)
- ✅ **Typography** (professional, readable fonts)
- ✅ **Visual Elements** (styled tables, callout boxes, citations)

### Compatibility
- ✅ **Yoast SEO** optimized
- ✅ **SEMRush** compliant
- ✅ **Google Search Console** ready
- ✅ **W3C HTML5** valid

## 📖 Usage

### Basic Usage

```bash
python3 blog_generator.py
```

This generates a blog post with the placeholder `[KEYWORD]` that you can replace with your actual keyword.

### Custom Keyword Usage

```python
from blog_generator import BlogPostGenerator

# Create a generator with your keyword
generator = BlogPostGenerator("Solar Panel Efficiency")

# Generate the complete HTML
html_content = generator.generate_full_html()

# Save to file
with open("solar_panel_efficiency.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

### Advanced Usage

```python
from blog_generator import BlogPostGenerator

# Initialize with your keyword
keyword = "Residential Solar Battery Storage"
generator = BlogPostGenerator(keyword)

# Access individual components
meta_title = generator.generate_meta_title()
meta_desc = generator.generate_meta_description()
slug = generator.slug
schema_json = generator.generate_schema_json()

# Generate full HTML
html = generator.generate_full_html()

# Save the output
output_file = f"blog_post_{slug}.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✓ Generated: {output_file}")
```

## 📁 Output Files

When you run the generator, it creates:

1. **`blog_post_[slug].html`** - The complete HTML blog post
2. **`blog_post_[slug]_metadata.json`** - Metadata file containing:
   - Keyword
   - Slug
   - Meta title
   - Meta description
   - Publication date
   - URL

## 🎨 Customization

### Modifying the Template

The generator uses a class-based approach. You can extend or modify:

```python
class CustomBlogGenerator(BlogPostGenerator):
    def generate_meta_title(self):
        # Custom meta title logic
        return f"{self.keyword} - Your Custom Suffix"
    
    def generate_chart_html(self):
        # Custom chart implementation
        return "<div>Your custom chart</div>"
```

### Styling

The CSS is embedded in the HTML template. To customize colors, fonts, or layout:

1. Edit the `<style>` section in `blog_generator.py`
2. Modify color variables (primary: `#ff6b35`, text: `#2c3e50`)
3. Adjust typography or spacing as needed

## 🔍 SEO Best Practices Implemented

### On-Page SEO
- ✅ Single H1 tag per page
- ✅ Logical heading hierarchy (H1 → H2 → H3)
- ✅ Keyword placement in title, headings, and content
- ✅ Meta description with call-to-action
- ✅ Alt text ready structure for images
- ✅ Internal linking to related content
- ✅ External links to authoritative sources

### Technical SEO
- ✅ Clean, semantic HTML5
- ✅ Mobile-responsive design
- ✅ Fast-loading inline CSS
- ✅ Schema.org structured data
- ✅ Proper character encoding (UTF-8)
- ✅ SEO-friendly URL structure

### Content SEO
- ✅ 1500+ word count (comprehensive)
- ✅ Natural keyword integration
- ✅ Topic clusters and subtopics
- ✅ Citations and references
- ✅ Data-driven content (charts/tables)
- ✅ Clear, scannable formatting

## 📊 Word Count

The generated blog posts exceed **1500 words** of expert-level content, ensuring:
- Better search engine rankings
- Comprehensive topic coverage
- Higher user engagement
- Authority building

## 🔗 Links Structure

### Internal Link
Points to `https://www.solartopps.com/commercial-solar/` (customizable)

### External Link
Points to `https://www.energy.gov/renewable-energy` (authoritative source)

Both links use proper attributes:
- Internal: `class="internal-link"`
- External: `class="external-link" target="_blank" rel="noopener"`

## 📈 Chart/Data Visualization

Includes a professionally styled HTML table with:
- Comparison metrics
- Statistical data
- Performance indicators
- Environmental impact data
- Responsive design
- Inline styles for portability

## 🎯 Matching SolarTopps Style

The generator produces content that matches the tone and style of:
`https://www.solartopps.com/blog/kilowatt-hour-kwh-vs-megawatt-hour-mwh/`

Key style elements:
- Professional, expert-level tone
- Educational approach
- Data-driven content
- Clear explanations
- Practical applications
- Visual data presentation

## 🛠️ Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 📝 Example Output

```
✓ Generated blog post: blog_post_keyword.html
✓ Slug: keyword
✓ Meta Title: [KEYWORD] | Complete Expert Guide 2025
✓ Meta Description: Expert guide to [KEYWORD]. Learn everything...
✓ Word count: 2347 words
✓ Generated metadata: blog_post_keyword_metadata.json

Blog post features:
  • H1, H2, and H3 heading structure
  • SEO-optimized meta title and description
  • URL-friendly slug generation
  • Schema.org BlogPosting JSON-LD
  • Inline citations [1-7]
  • 1 internal link to SolarTopps
  • 1 external link to authoritative source
  • HTML chart/table with comparison data
  • Open Graph and Twitter Card meta tags
  • Mobile-responsive CSS styling
  • Professional formatting matching SolarTopps style
  • 1500+ word expert-level content
```

## 🚀 Quick Start

1. Clone the repository
2. Run the generator:
   ```bash
   python3 blog_generator.py
   ```
3. Open `blog_post_keyword.html` in a browser to preview
4. Replace `[KEYWORD]` with your actual keyword throughout the content
5. Upload to your CMS or website

## 📄 License

This tool is designed for SolarTopps.com content creation.

## 🤝 Contributing

To improve the generator:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For questions or issues, please open a GitHub issue.

---

**Generated with ST-ARC** - Professional blog post generation for SolarTopps.com
