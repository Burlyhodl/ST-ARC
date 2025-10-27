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
"""
Example usage of the SEO Blog Generator for SolarTopps
Demonstrates both programmatic and CLI usage
"""

from seo_blog_generator import SEOBlogGenerator


def example_programmatic_usage():
    """Example of using the generator programmatically"""
    
    # Initialize the generator
    generator = SEOBlogGenerator()
    
    # Example reference content
    reference_content = """
    Solar energy has become increasingly popular in recent years. 
    The cost of solar panels has decreased significantly, making it more 
    accessible to homeowners. Battery storage systems like the Tesla Powerwall 
    have revolutionized how homeowners can store and use solar energy.
    """
    
    # Target keyword
    keyword = "Tesla Powerwall installation cost"
    
    # Secondary keywords
    secondary_keywords = ["solar battery storage", "home energy storage", "powerwall price"]
    
    # Custom slug
    slug = "tesla-powerwall-installation-cost-guide"
    
    # Custom data for visualization
    data_points = {
        'labels': ['2020', '2021', '2022', '2023', '2024'],
        'values': [15, 23, 35, 48, 62],
        'title': 'Solar Battery Installation Growth (%)'
    }
    
    # Generate the blog post
    result = generator.generate_wordpress_html(
        input_content=reference_content,
        keyword=keyword,
        secondary_keywords=secondary_keywords,
        custom_slug=slug,
        data_points=data_points
    )
    
    # Display results
    print("Generated Blog Post")
    print("=" * 80)
    print(f"Title: {result['title']}")
    print(f"Slug: {result['slug']}")
    print(f"Meta Description: {result['meta_description']}")
    print(f"Word Count: {result['word_count']}")
    print()
    
    print("Links Used:")
    for i, link in enumerate(result['links'], 1):
        print(f"{i}. {link['anchor_text']} -> {link['url']}")
    print()
    
    # Save to file
    output_file = f"example_blog_{result['slug']}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result['content'])
    
    print(f"Saved to: {output_file}")
    
    return result


def example_url_fetch():
    """Example of fetching content from a URL"""
    
    generator = SEOBlogGenerator()
    
    # Example: Fetch from a solar energy URL
    # url = "https://www.energy.gov/solar-energy"
    # content = generator.fetch_url_content(url)
    
    # For this example, we'll use placeholder content
    content = "Solar energy reference content from URL"
    
    keyword = "residential solar panel systems"
    
    result = generator.generate_wordpress_html(
        input_content=content,
        keyword=keyword
    )
    
    print(f"Generated blog post with {result['word_count']} words")
    print(f"Slug: {result['slug']}")
    
    return result


def example_custom_visualization():
    """Example with custom data visualization"""
    
    generator = SEOBlogGenerator()
    
    # Custom solar cost data
    cost_data = {
        'labels': ['5kW System', '7kW System', '10kW System', '15kW System'],
        'values': [15000, 20000, 28000, 38000],
        'title': 'Average Solar System Costs (Before Incentives)'
    }
    
    result = generator.generate_wordpress_html(
        input_content="Solar system costs vary by size and location",
        keyword="solar system cost breakdown",
        data_points=cost_data
    )
    
    print(f"Generated with custom cost visualization")
    print(f"Title: {result['title']}")
    
    return result


def example_complete_workflow():
    """Complete workflow example with all features"""
    
    print("=" * 80)
    print("COMPLETE SEO BLOG GENERATION WORKFLOW")
    print("=" * 80)
    print()
    
    generator = SEOBlogGenerator()
    
    # Step 1: Define your content parameters
    print("Step 1: Defining content parameters...")
    reference = """
    The Tesla Powerwall is a home battery system that stores energy from solar panels 
    or the grid. It provides backup power during outages and helps reduce electricity bills.
    Installation costs vary by location, with Arizona having favorable conditions for solar.
    """
    
    primary_kw = "Tesla Powerwall installation cost Arizona"
    secondary_kws = ["Powerwall price Arizona", "solar battery cost", "home energy storage"]
    
    # Step 2: Prepare data visualization
    print("Step 2: Preparing data visualization...")
    viz_data = {
        'labels': ['Equipment', 'Installation', 'Permits', 'Total'],
        'values': [11500, 1500, 500, 13500],
        'title': 'Tesla Powerwall Cost Breakdown in Arizona'
    }
    
    # Step 3: Generate the blog post
    print("Step 3: Generating SEO-optimized blog post...")
    result = generator.generate_wordpress_html(
        input_content=reference,
        keyword=primary_kw,
        secondary_keywords=secondary_kws,
        custom_slug="tesla-powerwall-cost-arizona",
        data_points=viz_data
    )
    
    # Step 4: Review results
    print("Step 4: Reviewing results...")
    print()
    print(f"✅ Title: {result['title']}")
    print(f"✅ Slug: {result['slug']}")
    print(f"✅ Meta Description: {result['meta_description']}")
    print(f"✅ Word Count: {result['word_count']} words")
    print(f"✅ Links: {len(result['links'])} external links")
    print()
    
    # Step 5: Save output
    print("Step 5: Saving output...")
    filename = f"complete_example_{result['slug']}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result['content'])
    
    print(f"✅ Saved to: {filename}")
    print()
    
    # Display schema snippet
    print("JSON-LD Schema (snippet):")
    print(result['schema'][:200] + "...")
    print()
    
    print("=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    # Run the complete workflow example
    example_complete_workflow()
    
    print("\n\nOther examples available:")
    print("- example_programmatic_usage()")
    print("- example_url_fetch()")
    print("- example_custom_visualization()")
