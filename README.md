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
