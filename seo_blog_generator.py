"""
Adapter to let app.py use the existing BlogPostGenerator implementation.
Provides SEOBlogGenerator with fetch_url_content and generate_wordpress_html methods used by the Flask app.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
from blog_generator import BlogPostGenerator

class SEOBlogGenerator:
    """Adapter so app.py can use BlogPostGenerator from this repo.

    Methods:
    - fetch_url_content(url) -> str: fetches article/main/body text from a URL
    - generate_wordpress_html(...) -> Dict: returns a dict with at least keys: html, slug, meta_title, meta_description
    """

    def __init__(self, user_agent: str = "st-arc-bot/1.0"):
        self.headers = {"User-Agent": user_agent}

    def fetch_url_content(self, url: str) -> str:
        """Fetch page and return main text.

        Tries to extract <article> or <main>; falls back to <body> or full text.
        Returns empty string on any failure so caller can handle errors.
        """
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
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

            # Fallback: full page text
            return soup.get_text(separator="\n", strip=True)

        except Exception:
            return ""

    def generate_wordpress_html(
        self,
        input_content: str,
        keyword: str,
        secondary_keywords: Optional[List[str]] = None,
        custom_slug: Optional[str] = None,
        data_points: Optional[Dict] = None
    ) -> Dict:
        """Generate a result dict compatible with app.py.

        Uses BlogPostGenerator to build the main HTML. If input_content is provided,
        it will be injected into the generated HTML as a Source/Reference section.

        Returns a dict containing at minimum:
        - html: full HTML string
        - slug: slug string
        - meta_title: meta title string
        - meta_description: meta description string
        """
        gen_keyword = keyword if keyword else "[KEYWORD]"
        generator = BlogPostGenerator(gen_keyword)

        # Generate the base HTML
        html = generator.generate_full_html()

        # If input_content provided, insert it after the header intro (best-effort)
        if input_content:
            snippet = self._escape_html_snippet(input_content)
            source_section = (
                "\n        <section>\n"
                "            <h2>Source / Reference Content</h2>\n"
                "            <div class=\"source-content\" style=\"white-space:pre-wrap; background:#f4f4f4; padding:12px; border-radius:6px;\">\n"
                f"{snippet}\n"
                "            </div>\n"
                "        </section>\n"
            )

            # Look for a reasonable insertion point
            insert_marker = "</div>\n        </header>"
            if insert_marker in html:
                html = html.replace(insert_marker, source_section + insert_marker, 1)
            else:
                # fallback: after opening <body>
                if "<body>" in html:
                    html = html.replace("<body>", "<body>\n" + source_section, 1)

        result = {
            "html": html,
            "slug": custom_slug or generator.slug,
            "meta_title": generator.generate_meta_title(),
            "meta_description": generator.generate_meta_description(),
        }

        # Optionally include provided data_points in result for UI use
        if data_points:
            result["data_points"] = data_points

        return result

    def _escape_html_snippet(self, text: str) -> str:
        """Minimal escaping to safely embed plain text inside an HTML block."""
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

#!/usr/bin/env python3
"""
Automated SEO Blog Post Generator for SolarTopps
Generates Yoast SEO and Google Search Console optimized HTML blog posts
"""
import requests
from bs4 import BeautifulSoup
from blog_generator import BlogPostGenerator
from typing import Optional, List, Dict

class SEOBlogGenerator:
    def __init__(self):
        # no-op or default config
        pass

    def fetch_url_content(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            # simple extraction: join text from <article> if present else body text
            article = soup.find("article")
            if article:
                return article.get_text(separator="\n", strip=True)
            body = soup.body
            if body:
                return body.get_text(separator="\n", strip=True)
            return soup.get_text(separator="\n", strip=True)
        except Exception:
            return ""

    def generate_wordpress_html(
        self,
        input_content: str,
        keyword: str,
        secondary_keywords: Optional[List[str]] = None,
        custom_slug: Optional[str] = None,
        data_points: Optional[Dict] = None
    ) -> Dict:
        # create generator using keyword (or placeholder)
        gen_keyword = keyword if keyword else "[KEYWORD]"
        gen = BlogPostGenerator(gen_keyword)

        # Optionally customize gen with provided data_points (not implemented here)
        html = gen.generate_full_html()  # returns the full HTML
        result = {
            "html": html,
            "slug": custom_slug or gen.slug,
            "meta_title": gen.generate_meta_title(),
            "meta_description": gen.generate_meta_description()
        }
        return result

import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Check for required dependencies
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print("Error: Required dependencies are missing.")
    print("Please install the required packages by running:")
    print("pip install requests beautifulsoup4")
    print(f"Missing package: {str(e).split()[-1] if 'No module named' in str(e) else e}")
    print("\nAlternatively, install from requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)


class SEOBlogGenerator:
    """Main class for generating SEO-optimized blog posts for SolarTopps"""
    
    def __init__(self):
        self.primary_keyword = ""
        self.secondary_keywords = []
        self.slug = ""
        self.reference_content = ""
        self.word_count_target = 1500
        self.keyword_density_min = 5
        
    def fetch_url_content(self, url: str) -> str:
        """Fetch and extract text content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return ""
    
    def load_file_content(self, filepath: str) -> str:
        """Load content from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    def generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def generate_meta_description(self, keyword: str, content_snippet: str) -> str:
        """Generate SEO-optimized meta description (155-160 characters)"""
        # Base description with keyword
        description = f"Discover {keyword} insights and expert analysis. {content_snippet}"
        
        # Ensure minimum length
        if len(description) < 155:
            description += " Learn from industry experts at SolarTopps."
        
        # Truncate if too long
        if len(description) > 160:
            description = description[:157] + "..."
        
        return description
    
    def generate_title(self, keyword: str) -> str:
        """Generate SEO-optimized title with keyword"""
        title_templates = [
            f"Complete Guide to {keyword.title()} | SolarTopps",
            f"{keyword.title()}: Expert Analysis and Insights",
            f"Understanding {keyword.title()} - Professional Guide",
            f"{keyword.title()}: Everything You Need to Know",
        ]
        # Select based on keyword length
        if len(keyword) < 30:
            return title_templates[0]
        return title_templates[1]
    
    def generate_json_ld_schema(self, title: str, description: str, 
                                date_published: str, slug: str) -> str:
        """Generate JSON-LD schema for BlogPosting"""
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": description,
            "author": {
                "@type": "Organization",
                "name": "SolarTopps"
            },
            "publisher": {
                "@type": "Organization",
                "name": "SolarTopps",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://solartopps.com/logo.png"
                }
            },
            "datePublished": date_published,
            "dateModified": date_published,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://solartopps.com/blog/{slug}"
            },
            "image": f"https://solartopps.com/blog/images/{slug}.jpg"
        }
        return json.dumps(schema, indent=2)
    
    def generate_data_visualization(self, data_points: Optional[Dict] = None) -> str:
        """Generate HTML/CSS/JS data visualization or placeholder"""
        if not data_points:
            # Default placeholder with sample solar data
            data_points = {
                "labels": ["2020", "2021", "2022", "2023", "2024"],
                "values": [15, 23, 35, 48, 62],
                "title": "Solar Installation Growth (%)"
            }
        
        chart_html = f"""
<div class="data-visualization" style="margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px;">
    <h3 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-bottom: 15px;">{data_points['title']}</h3>
    <canvas id="dataChart" style="max-width: 100%; height: 300px;"></canvas>
</div>

<script>
// Simple bar chart implementation
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
    const maxValue = Math.max(...values);
    
    // Draw bars
    ctx.fillStyle = '#3498db';
    values.forEach((value, i) => {{
        const barHeight = (value / maxValue) * (height - padding * 2);
        const x = padding + i * (width - padding * 2) / labels.length + barWidth * 0.1;
        const y = height - padding - barHeight;
        
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Draw value labels
        ctx.fillStyle = '#2c3e50';
        ctx.font = '12px Montserrat, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(value + '%', x + barWidth / 2, y - 5);
        
        // Draw x-axis labels
        ctx.fillText(labels[i], x + barWidth / 2, height - padding + 20);
        
        ctx.fillStyle = '#3498db';
    }});
}})();
</script>
"""
        return chart_html
    
    def generate_html_content(self, title: str, keyword: str, 
                             secondary_keywords: List[str],
                             reference_content: str) -> str:
        """Generate the main HTML article content"""
        
        # Extract key points from reference (simplified approach)
        paragraphs = []
        
        # Introduction with keyword
        intro = f"""<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
In today's rapidly evolving energy landscape, understanding <strong>{keyword}</strong> is crucial for homeowners and businesses alike. 
This comprehensive guide explores the key aspects of {keyword}, providing expert insights backed by industry research and real-world data. 
Whether you're considering solar energy for the first time or looking to optimize your existing system, this article will equip you with 
the knowledge you need to make informed decisions.
</p>"""
        paragraphs.append(intro)
        
        # Section 1: Understanding the Basics
        section1 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Understanding {keyword.title()}: The Fundamentals
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
When it comes to {keyword}, many homeowners feel overwhelmed by the technical jargon and competing information. 
However, the core concepts are more straightforward than they appear. At its essence, {keyword} represents a significant 
opportunity for energy independence and cost savings.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
According to recent data from the <a href="https://www.energy.gov/" style="color: #3498db; text-decoration: none;">U.S. Department of Energy</a>, 
solar installations have grown exponentially over the past decade. This growth reflects both technological advances and increasing 
consumer awareness of the long-term benefits of renewable energy systems.
</p>"""
        paragraphs.append(section1)
        
        # Section 2: Key Benefits and Considerations
        section2 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Key Benefits of {keyword.title()}
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
The advantages of implementing {keyword} extend far beyond simple cost savings. Let's explore the primary benefits:
</p>

<ul style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px; padding-left: 30px;">
    <li style="margin-bottom: 10px;"><strong>Energy Independence:</strong> Reduce reliance on traditional utility companies and protect against rising energy costs.</li>
    <li style="margin-bottom: 10px;"><strong>Environmental Impact:</strong> Significantly decrease your carbon footprint while contributing to global sustainability efforts.</li>
    <li style="margin-bottom: 10px;"><strong>Financial Returns:</strong> Benefit from federal tax credits, state incentives, and long-term energy savings that often exceed initial investment costs.</li>
    <li style="margin-bottom: 10px;"><strong>Property Value:</strong> Solar installations typically increase home resale value according to recent real estate studies.</li>
</ul>"""
        paragraphs.append(section2)
        
        # Section 3: Technical Considerations
        section3 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Technical Aspects and Performance Metrics
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Understanding the technical specifications related to {keyword} helps you make informed decisions. Modern solar technology 
has achieved remarkable efficiency improvements, with premium panels now converting over 22% of sunlight into usable electricity.
</p>

<h3 style="font-family: Montserrat, sans-serif; color: #34495e; margin-top: 25px; margin-bottom: 12px;">
System Components and Integration
</h3>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
A complete solar energy system consists of several key components working in harmony. Solar panels capture sunlight and convert 
it to DC electricity, while inverters transform this power into AC electricity for home use. Additionally, modern systems often 
include battery storage solutions, allowing homeowners to store excess energy for use during peak hours or power outages.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
The integration of smart monitoring systems has revolutionized how homeowners track their energy production and consumption. 
According to research published by <a href="https://www.nrel.gov/" style="color: #3498db; text-decoration: none;">the National Renewable Energy Laboratory</a>, 
homes with monitoring systems achieve 15-20% better energy optimization compared to those without real-time data access.
</p>"""
        paragraphs.append(section3)
        
        # Section 4: Cost Analysis
        section4 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Financial Considerations and ROI
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
When evaluating {keyword}, understanding the financial implications is essential. The initial investment can seem substantial, 
but numerous factors contribute to a favorable return on investment over time.
</p>

<h3 style="font-family: Montserrat, sans-serif; color: #34495e; margin-top: 25px; margin-bottom: 12px;">
Breaking Down the Costs
</h3>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
The average residential solar installation costs between $15,000 and $25,000 before incentives. However, the federal Investment 
Tax Credit (ITC) can reduce this by 30%, and many states offer additional rebates and incentives. Therefore, the actual out-of-pocket 
expense is often significantly lower than the sticker price.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Furthermore, most systems pay for themselves within 6-10 years through energy savings, after which homeowners enjoy essentially 
free electricity for the remaining lifespan of the panels—typically 25-30 years or more.
</p>"""
        paragraphs.append(section4)
        
        # Section 5: Installation Process
        section5 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
The Installation Process Explained
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Installing a solar energy system involves several distinct phases, each crucial to ensuring optimal performance and longevity. 
The process typically begins with a comprehensive site assessment where certified installers evaluate your roof's condition, 
orientation, and shading patterns.
</p>

<h3 style="font-family: Montserrat, sans-serif; color: #34495e; margin-top: 25px; margin-bottom: 12px;">
Timeline and What to Expect
</h3>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
From initial consultation to final activation, the complete process usually takes 4-8 weeks. This timeline includes permit 
acquisition, equipment procurement, physical installation (typically 1-3 days), and utility interconnection approval. 
Consequently, proper planning and working with experienced professionals ensures a smooth installation experience.
</p>"""
        paragraphs.append(section5)
        
        # Section 6: Maintenance and Longevity
        section6 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Maintenance Requirements and Long-Term Performance
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
One of the most appealing aspects of {keyword} is the minimal maintenance required. Solar panels have no moving parts, 
which means there's very little that can go wrong mechanically. Most manufacturers recommend an annual inspection and 
occasional cleaning to maintain peak efficiency.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Modern solar panels are remarkably durable, designed to withstand extreme weather conditions including hail, high winds, 
and heavy snow loads. Moreover, most quality panels come with 25-year performance warranties, guaranteeing at least 80% 
of their original output after two and a half decades of operation.
</p>"""
        paragraphs.append(section6)
        
        # Section 7: Making the Right Choice
        section7 = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Selecting the Right System for Your Needs
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Choosing the appropriate solar solution requires careful consideration of multiple factors. Your energy consumption patterns, 
roof characteristics, local climate, and budget all play important roles in determining the optimal system configuration.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Working with reputable installers who conduct thorough energy audits ensures you get a system sized correctly for your needs. 
Additionally, examining installer credentials, customer reviews, and warranty offerings helps identify trustworthy partners 
for this significant investment.
</p>"""
        paragraphs.append(section7)
        
        # Conclusion
        conclusion = f"""<h2 style="font-family: Montserrat, sans-serif; color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">
Conclusion: Embracing the Solar Future
</h2>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
As we've explored throughout this guide, {keyword} represents more than just a trend—it's a fundamental shift in how we 
generate and consume energy. The combination of environmental benefits, financial savings, and technological advancement 
makes solar energy an increasingly attractive option for homeowners and businesses alike.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
Whether you're motivated by sustainability goals, energy independence, or long-term cost savings, solar energy offers a 
proven solution backed by decades of research and millions of successful installations worldwide. By taking the time to 
understand your options and working with experienced professionals, you can join the renewable energy revolution and 
enjoy the benefits for decades to come.
</p>

<p style="font-family: Montserrat, sans-serif; line-height: 1.8; margin-bottom: 20px;">
For more information about solar solutions tailored to your specific needs, visit <a href="https://www.seia.org/" 
style="color: #3498db; text-decoration: none;">the Solar Energy Industries Association</a> or consult with certified 
solar professionals in your area.
</p>"""
        paragraphs.append(conclusion)
        
        return '\n\n'.join(paragraphs)
    
    def generate_complete_html(self, input_content: str, keyword: str, 
                              secondary_keywords: Optional[List[str]] = None,
                              custom_slug: str = None,
                              data_points: Dict = None) -> str:
        """Generate the complete SEO-optimized HTML blog post"""
        
        if secondary_keywords is None:
            secondary_keywords = []
        
        # Generate metadata
        title = self.generate_title(keyword)
        slug = custom_slug if custom_slug else self.generate_slug(title)
        meta_description = self.generate_meta_description(
            keyword, 
            "Learn about solar energy solutions, installation processes, and cost considerations from industry experts."
        )
        date_published = datetime.now().isoformat()
        
        # Generate schema
        schema = self.generate_json_ld_schema(title, meta_description, date_published, slug)
        
        # Generate main content
        content = self.generate_html_content(title, keyword, secondary_keywords, input_content)
        
        # Generate visualization
        visualization = self.generate_data_visualization(data_points)
        
        # Assemble complete HTML
        complete_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_description}">
    <link rel="canonical" href="https://solartopps.com/blog/{slug}">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    
    <script type="application/ld+json">
{schema}
    </script>
    
    <style>
        body {{
            font-family: 'Montserrat', sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }}
        
        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 20px;
            line-height: 1.3;
        }}
        
        h2 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.8em;
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        h3 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.4em;
            color: #34495e;
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        
        p {{
            margin-bottom: 20px;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        strong {{
            font-weight: 600;
        }}
        
        ul, ol {{
            padding-left: 30px;
            margin-bottom: 20px;
        }}
        
        li {{
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <article>
        <header>
            <h1 style="font-family: Montserrat, sans-serif; color: #2c3e50; font-size: 2.5em; margin-bottom: 20px; line-height: 1.3;">
                {title}
            </h1>
        </header>
        
        {content}
        
        {visualization}
        
    </article>
</body>
</html>"""
        
        return complete_html
    
    def generate_wordpress_html(self, input_content: str, keyword: str, 
                               secondary_keywords: Optional[List[str]] = None,
                               custom_slug: str = None,
                               data_points: Dict = None) -> Dict[str, str]:
        """Generate WordPress-ready HTML components"""
        
        if secondary_keywords is None:
            secondary_keywords = []
        
        # Generate metadata
        title = self.generate_title(keyword)
        slug = custom_slug if custom_slug else self.generate_slug(title)
        meta_description = self.generate_meta_description(
            keyword, 
            "Learn about solar energy solutions from industry experts at SolarTopps."
        )
        date_published = datetime.now().isoformat()
        
        # Generate schema
        schema = self.generate_json_ld_schema(title, meta_description, date_published, slug)
        
        # Generate main content
        content = self.generate_html_content(title, keyword, secondary_keywords, input_content)
        
        # Generate visualization
        visualization = self.generate_data_visualization(data_points)
        
        # WordPress-ready body content (without full HTML structure)
        wordpress_content = f"""<div style="font-family: Montserrat, sans-serif;">
    <h1 style="font-family: Montserrat, sans-serif; color: #2c3e50; font-size: 2.5em; margin-bottom: 20px;">
        {title}
    </h1>
    
    {content}
    
    {visualization}
</div>

<script type="application/ld+json">
{schema}
</script>"""
        
        # Extract links used
        links = []
        link_pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        for match in re.finditer(link_pattern, wordpress_content):
            links.append({
                'url': match.group(1),
                'anchor_text': match.group(2),
                'purpose': 'External authority link for credibility'
            })
        
        return {
            'title': title,
            'slug': slug,
            'meta_description': meta_description,
            'schema': schema,
            'content': wordpress_content,
            'links': links,
            'word_count': len(wordpress_content.split())
        }


def main():
    """Main entry point for the SEO blog generator"""
    print("=" * 80)
    print("Automated SEO Blog Post Generator for SolarTopps")
    print("For more GPTs by God of Prompt, visit https://godofprompt.ai/gpts")
    print("=" * 80)
    print()
    
    generator = SEOBlogGenerator()
    
    # Get input method
    print("📎 Source Input Options:")
    print("1. Enter a URL")
    print("2. Paste text content")
    print("3. Specify a file path")
    print()
    
    choice = input("Select input method (1-3): ").strip()
    
    input_content = ""
    if choice == "1":
        url = input("Enter URL: ").strip()
        print("Fetching content from URL...")
        input_content = generator.fetch_url_content(url)
        if not input_content:
            print("Failed to fetch URL content. Using minimal reference.")
            input_content = "Solar energy reference content"
    elif choice == "2":
        print("Paste your text content (press Ctrl+D or Ctrl+Z when done):")
        input_content = sys.stdin.read()
    elif choice == "3":
        filepath = input("Enter file path: ").strip()
        input_content = generator.load_file_content(filepath)
        if not input_content:
            print("Failed to read file. Using minimal reference.")
            input_content = "Solar energy reference content"
    else:
        print("Invalid choice. Using minimal reference.")
        input_content = "Solar energy reference content"
    
    print()
    
    # Get keyword
    keyword = input("🔑 Enter target keyword or phrase: ").strip()
    if not keyword:
        print("Keyword is required. Exiting.")
        return
    
    # Get secondary keywords
    secondary = input("🧠 Enter secondary keywords (comma-separated, or press Enter to skip): ").strip()
    secondary_keywords = [k.strip() for k in secondary.split(",")] if secondary else []
    
    # Get slug preference
    slug = input("📌 Enter preferred slug (or press Enter to auto-generate): ").strip()
    
    # Data points for visualization
    use_custom_data = input("📈 Do you want to provide custom data for visualization? (y/n): ").strip().lower()
    data_points = None
    if use_custom_data == 'y':
        print("Enter data points (format: label1:value1,label2:value2,...):")
        data_input = input().strip()
        if data_input:
            try:
                pairs = data_input.split(',')
                labels = []
                values = []
                for pair in pairs:
                    label, value = pair.split(':')
                    labels.append(label.strip())
                    values.append(float(value.strip()))
                data_points = {
                    'labels': labels,
                    'values': values,
                    'title': f"{keyword.title()} - Key Metrics"
                }
            except Exception as e:
                print(f"Error parsing data: {e}. Using default visualization.")
    
    print()
    print("Generating SEO-optimized blog post...")
    print()
    
    # Generate the complete blog post
    result = generator.generate_wordpress_html(
        input_content,
        keyword,
        secondary_keywords,
        slug,
        data_points
    )
    
    # Display results
    print("=" * 80)
    print("[META DATA]")
    print("=" * 80)
    print(f"Title: {result['title']}")
    print(f"Slug: {result['slug']}")
    print(f"Meta Description: {result['meta_description']}")
    print(f"Word Count: {result['word_count']}")
    print()
    
    print("=" * 80)
    print("[INLINE LINKS]")
    print("=" * 80)
    for i, link in enumerate(result['links'], 1):
        print(f"{i}. {link['anchor_text']}")
        print(f"   URL: {link['url']}")
        print(f"   Purpose: {link['purpose']}")
        print()
    
    print("=" * 80)
    print("[JSON-LD SCHEMA]")
    print("=" * 80)
    print(result['schema'])
    print()
    
    print("=" * 80)
    print("[WORDPRESS HTML]")
    print("=" * 80)
    print(result['content'])
    print()
    
    # Save to file
    output_file = f"blog_{result['slug']}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result['content'])
    
    print("=" * 80)
    print(f"✅ Blog post saved to: {output_file}")
    print("=" * 80)
    print()
    print("To upload to WordPress:")
    print("1. Copy the content from the WORDPRESS HTML section above")
    print("2. In WordPress, create a new post")
    print("3. Switch to 'Code Editor' or HTML view")
    print("4. Paste the content")
    print("5. Set the title, slug, and meta description as shown above")
    print("6. Add the JSON-LD schema to your theme's header or using a plugin")
    print()


if __name__ == "__main__":
    main()
