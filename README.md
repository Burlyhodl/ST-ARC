# ST-ARC - Automated SEO Blog Post Generator for SolarTopps

ST-Article Creator and AI article generator that creates fully optimized, expert-level blog content for SolarTopps.com that meets Yoast SEO, Google Search Console, and SEMrush standards.

## Features

✅ **1500+ word minimum content** - Professional, comprehensive articles  
✅ **Yoast SEO compliant** - Green scores for both SEO and Readability  
✅ **Raw HTML output** - Ready for WordPress block editor  
✅ **JSON-LD Schema** - BlogPosting structured data for enhanced Google AI understanding  
✅ **SEO-optimized metadata** - Title, meta description, slug generation  
✅ **Inline source links** - Descriptive anchor text that flows naturally  
✅ **Data visualization** - HTML/CSS/JS charts with solar industry data  
✅ **Multiple input methods** - URL, text, or file input supported  
✅ **Keyword optimization** - Primary and secondary keyword integration  
✅ **Font: Montserrat** - Professional, readable typography  

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Burlyhodl/ST-ARC.git
cd ST-ARC
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the generator in interactive mode:

```bash
python seo_blog_generator.py
```

You'll be prompted for:
- **Source Input**: URL, pasted text, or file path
- **Target Keyword**: Primary SEO focus keyword
- **Secondary Keywords**: Optional semantic variations (comma-separated)
- **Slug**: URL slug (auto-generated if not provided)
- **Data Visualization**: Optional custom data points for charts

### Example Workflow

```
📎 Source Input Options:
1. Enter a URL
2. Paste text content
3. Specify a file path

Select input method (1-3): 1
Enter URL: https://example.com/solar-article

🔑 Enter target keyword or phrase: Tesla Powerwall installation cost Arizona

🧠 Enter secondary keywords (comma-separated, or press Enter to skip): 
powerwall cost, battery storage Arizona, solar battery installation

📌 Enter preferred slug (or press Enter to auto-generate): 
tesla-powerwall-installation-cost-arizona

📈 Do you want to provide custom data for visualization? (y/n): y
Enter data points (format: label1:value1,label2:value2,...):
2020:15,2021:23,2022:35,2023:48,2024:62

Generating SEO-optimized blog post...
```

## Output Structure

The generator produces:

### 1. **Meta Data**
- SEO-optimized title (with keyword)
- URL-friendly slug
- Meta description (155-160 chars)
- Word count statistics

### 2. **HTML Content**
- H1 title with keyword
- Multiple H2 and H3 headings
- 1500+ words of optimized content
- Montserrat font styling
- Short paragraphs (2-5 lines)
- Transition words (>30%)
- Passive voice (<10%)

### 3. **Data Visualization**
- HTML/CSS/JS bar chart
- Customizable or default solar data
- Responsive design
- Professional styling

### 4. **JSON-LD Schema**
- BlogPosting structured data
- Publisher information
- Date metadata
- Canonical URL

### 5. **Inline Links**
- Descriptive anchor text
- Authority sources (.gov, .edu)
- Natural sentence integration
- Purpose documentation

## SEO Optimization Features

### Keyword Usage
- ✅ Primary keyword in title
- ✅ Primary keyword in first paragraph
- ✅ Primary keyword in at least one H2 heading
- ✅ Minimum 5 keyword instances throughout article
- ✅ Natural keyword distribution

### Readability
- ✅ Short paragraphs (2-5 lines)
- ✅ Transition words (>30%)
- ✅ Active voice (>90%)
- ✅ Subheadings every 300 words
- ✅ Bullet points and lists
- ✅ Clear, accessible language

### Technical SEO
- ✅ Semantic HTML5 structure
- ✅ Meta tags optimized
- ✅ Schema.org markup
- ✅ Mobile-responsive design
- ✅ Fast-loading charts
- ✅ Canonical URL

## WordPress Integration

### Manual Upload
1. Copy the generated HTML from the output
2. In WordPress, create a new post
3. Switch to "Code Editor" or HTML block
4. Paste the HTML content
5. Set the title, slug, and meta description
6. Add JSON-LD schema via theme header or SEO plugin

### API Upload (Advanced)
The generator outputs WordPress-ready HTML that can be posted via REST API:

```python
import requests

# WordPress site credentials
wp_url = "https://solartopps.com/wp-json/wp/v2/posts"
wp_user = "your_username"
wp_password = "your_app_password"

# Post data
post_data = {
    "title": result['title'],
    "content": result['content'],
    "slug": result['slug'],
    "status": "draft",  # or "publish"
    "meta": {
        "description": result['meta_description']
    }
}

# Make request
response = requests.post(
    wp_url,
    json=post_data,
    auth=(wp_user, wp_password)
)
```

## Yoast SEO Compliance

The generator ensures green scores for:

### SEO Analysis
- ✅ Keyphrase in title
- ✅ Keyphrase in meta description
- ✅ Keyphrase in introduction
- ✅ Keyphrase in subheading
- ✅ Keyphrase density (0.5-2.5%)
- ✅ Meta description length
- ✅ Text length (>300 words)
- ✅ Outbound links
- ✅ Image alt attributes (when images added)

### Readability Analysis
- ✅ Subheading distribution
- ✅ Paragraph length (<150 words)
- ✅ Sentence length (<20 words avg)
- ✅ Transition words
- ✅ Passive voice
- ✅ Flesch Reading Ease

## Example Output Files

Generated files are saved as `blog_{slug}.html` in the current directory.

Example: `blog_tesla-powerwall-installation-cost-arizona.html`

## Customization

### Modify Content Structure
Edit `generate_html_content()` method to adjust:
- Section headings
- Content flow
- Paragraph structure
- List formats

### Adjust SEO Parameters
Modify class attributes:
```python
generator.word_count_target = 2000  # Change word count
generator.keyword_density_min = 7   # Adjust keyword frequency
```

### Custom Chart Styles
Edit `generate_data_visualization()` to customize:
- Chart type (bar, line, pie)
- Colors and styling
- Data format
- Responsive behavior

## Best Practices

### Keywords
- Choose specific, realistic keywords (e.g., "solar panel installation Phoenix AZ")
- Avoid overly broad terms
- Use semantic variations naturally
- Research keyword volume and competition

### Content Input
- Provide high-quality reference material
- Use trusted sources for citations
- Include relevant statistics and data
- Ensure factual accuracy

### Citations
- Link to authoritative sources (.gov, .edu, industry leaders)
- Use descriptive anchor text (not "click here")
- Ensure links are relevant and add value
- Mix internal and external links

## Troubleshooting

### URL Fetching Issues
If URL fetching fails:
- Check internet connection
- Verify URL is accessible
- Try using text input instead
- Check for CAPTCHA or blocking

### Keyword Not Appearing Enough
- Increase content length
- Add more relevant sections
- Use keyword variations
- Check keyword spelling

### Low Word Count
- Provide more detailed reference content
- Add more sections to template
- Expand on technical details
- Include more examples

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for SolarTopps content creation.

## Credits

For more GPTs by God of Prompt, visit https://godofprompt.ai/gpts

---

**Note**: This tool generates content based on reference materials and templates. Always review and edit generated content for accuracy, brand voice, and specific requirements before publishing.
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
ST-Article Creator and AI article generator

## Uploading Articles to WordPress

### Prerequisites

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a WordPress Application Password**
   - Log in to your WordPress site
   - Go to Users → Profile
   - Scroll to "Application Passwords"
   - Create a new application password for ST-ARC
   - Copy the generated password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### Method 1: Standalone Upload Script

Use this method to upload an existing HTML file to WordPress.

1. **Set your WordPress application password** as an environment variable:
   ```bash
   export WP_APPLICATION_PASSWORD="abcd efgh ijkl mnop qrst uvwx"
   ```

2. **Run the upload script** with your WordPress username and HTML file:
   ```bash
   python scripts/upload_to_wordpress.py content/solar-roi-playbook.html \
       --username your-wordpress-username \
       --status draft
   ```

3. **Available options:**
   - `--username USERNAME` (required): WordPress username
   - `--password PASSWORD` (optional): Application password (falls back to WP_APPLICATION_PASSWORD)
   - `--base-url URL` (optional): WordPress site URL (default: https://www.solartopps.com)
   - `--status {draft,publish,future}` (optional): Post status (default: draft)
   - `--categories ID [ID ...]` (optional): Category IDs to assign
   - `--tags ID [ID ...]` (optional): Tag IDs to assign
   - `--dry-run` (optional): Preview payload without uploading

4. **Test with dry-run first:**
   ```bash
   python scripts/upload_to_wordpress.py content/solar-roi-playbook.html \
       --username your-wordpress-username \
       --dry-run
   ```

### Method 2: Integrated Workflow Script

Use this method for end-to-end article generation and publishing.

1. **Publish an existing article:**
   ```bash
   python scripts/article_workflow.py publish \
       --file content/solar-roi-playbook.html \
       --username your-wordpress-username \
       --status draft
   ```

2. **Generate and publish in one command** (requires OpenAI API key):
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export WP_APPLICATION_PASSWORD="your-wp-password"
   
   python scripts/article_workflow.py generate \
       "Solar Panel Efficiency Tips" \
       --reference-url https://example.com/solar-article \
       --username your-wordpress-username \
       --status draft
   ```

### Metadata Extraction

The upload scripts automatically extract metadata from your HTML:
- **Title**: From `<title>` tag
- **Meta Description**: From `<meta name="description">` tag
- **Slug**: From `<strong>Slug:</strong>` in the HTML, or auto-generated from title

Example HTML structure:
```html
<head>
  <title>Solar Panel Installation Guide 2025</title>
  <meta name="description" content="Complete guide to solar panel installation." />
</head>
<body>
  <section id="meta_data">
    <p><strong>Slug:</strong> solar-panel-installation-guide</p>
  </section>
</body>
```

### Advanced Usage

**Upload with categories and tags:**
```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --categories 5 12 \
    --tags 8 15 22 \
    --status publish
```

**Change base URL for a different WordPress site:**
```bash
python scripts/upload_to_wordpress.py content/article.html \
    --username admin \
    --base-url https://yourblog.com \
    --password "your app password"
```

### Troubleshooting

**Authentication Error (401):**
- Verify your WordPress username is correct
- Regenerate your application password
- Check that WP_APPLICATION_PASSWORD environment variable is set

**Missing Metadata Error:**
- Ensure your HTML has a `<title>` tag
- Add a `<meta name="description">` tag
- The slug will be auto-generated if not present

**Connection Timeout:**
- Check your internet connection
- Verify the WordPress site URL is correct
- Try increasing the timeout (modify the script if needed)
