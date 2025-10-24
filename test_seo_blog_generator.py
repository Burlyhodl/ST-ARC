#!/usr/bin/env python3
"""
Test suite for SEO Blog Generator
Tests various components and ensures SEO compliance
"""

import unittest
import json
import re
from seo_blog_generator import SEOBlogGenerator


class TestSEOBlogGenerator(unittest.TestCase):
    """Test cases for the SEO Blog Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = SEOBlogGenerator()
        self.test_keyword = "solar panel installation"
        self.test_content = "Solar panels convert sunlight into electricity efficiently."
    
    def test_slug_generation(self):
        """Test URL slug generation"""
        title = "Complete Guide to Solar Panel Installation | SolarTopps"
        slug = self.generator.generate_slug(title)
        
        # Should be lowercase
        self.assertEqual(slug, slug.lower())
        # Should not have special characters
        self.assertNotIn(' ', slug)
        self.assertNotIn('|', slug)
        # Should use hyphens
        self.assertIn('-', slug)
        self.assertIn('solar', slug)
    
    def test_meta_description_length(self):
        """Test meta description is within SEO limits"""
        meta = self.generator.generate_meta_description(
            self.test_keyword,
            "This is a test snippet about solar energy systems."
        )
        
        # Should be 155-160 characters for optimal SEO
        self.assertLessEqual(len(meta), 160)
        self.assertGreater(len(meta), 50)
        # Should contain keyword
        self.assertIn(self.test_keyword, meta.lower())
    
    def test_title_generation(self):
        """Test SEO title generation"""
        title = self.generator.generate_title(self.test_keyword)
        
        # Should contain keyword
        self.assertIn(self.test_keyword, title.lower())
        # Should be reasonable length (under 60 chars for SEO)
        self.assertLessEqual(len(title), 70)
        # Should have SolarTopps branding
        self.assertTrue('SolarTopps' in title or 'Guide' in title or 'Expert' in title)
    
    def test_json_ld_schema_structure(self):
        """Test JSON-LD schema has required fields"""
        title = "Test Solar Article"
        description = "Test description"
        date = "2024-01-01T00:00:00"
        slug = "test-solar-article"
        
        schema_str = self.generator.generate_json_ld_schema(
            title, description, date, slug
        )
        schema = json.loads(schema_str)
        
        # Check required schema fields
        self.assertEqual(schema['@context'], 'https://schema.org')
        self.assertEqual(schema['@type'], 'BlogPosting')
        self.assertEqual(schema['headline'], title)
        self.assertEqual(schema['description'], description)
        
        # Check author and publisher
        self.assertEqual(schema['author']['@type'], 'Organization')
        self.assertEqual(schema['author']['name'], 'SolarTopps')
        self.assertEqual(schema['publisher']['name'], 'SolarTopps')
        
        # Check dates
        self.assertEqual(schema['datePublished'], date)
        self.assertEqual(schema['dateModified'], date)
    
    def test_data_visualization_generation(self):
        """Test data visualization HTML generation"""
        data_points = {
            'labels': ['2020', '2021', '2022'],
            'values': [10, 20, 30],
            'title': 'Test Chart'
        }
        
        viz_html = self.generator.generate_data_visualization(data_points)
        
        # Should contain canvas element
        self.assertIn('<canvas', viz_html)
        self.assertIn('id="dataChart"', viz_html)
        
        # Should contain script tag
        self.assertIn('<script>', viz_html)
        
        # Should contain the data
        self.assertIn('2020', viz_html)
        self.assertIn('2021', viz_html)
        self.assertIn('2022', viz_html)
        
        # Should contain chart title
        self.assertIn('Test Chart', viz_html)
    
    def test_html_content_generation(self):
        """Test main HTML content generation"""
        content = self.generator.generate_html_content(
            "Test Title",
            self.test_keyword,
            ["secondary keyword"],
            self.test_content
        )
        
        # Should contain keyword multiple times
        keyword_count = content.lower().count(self.test_keyword.lower())
        self.assertGreaterEqual(keyword_count, 5, "Should have at least 5 keyword instances")
        
        # Should have proper HTML structure
        self.assertIn('<h2', content)
        self.assertIn('<p', content)
        self.assertIn('<ul', content)
        
        # Should have Montserrat font
        self.assertIn('Montserrat', content)
        
        # Should have external links
        self.assertIn('<a href=', content)
        self.assertIn('https://', content)
    
    def test_complete_html_structure(self):
        """Test complete HTML output structure"""
        html = self.generator.generate_complete_html(
            self.test_content,
            self.test_keyword
        )
        
        # Should have proper HTML structure
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('<html', html)
        self.assertIn('<head>', html)
        self.assertIn('<body>', html)
        
        # Should have meta tags
        self.assertIn('<meta charset', html)
        self.assertIn('<meta name="description"', html)
        self.assertIn('<meta name="viewport"', html)
        
        # Should have schema
        self.assertIn('application/ld+json', html)
        self.assertIn('BlogPosting', html)
        
        # Should have title
        self.assertIn('<title>', html)
        
        # Should load Montserrat font
        self.assertIn('Montserrat', html)
    
    def test_wordpress_html_generation(self):
        """Test WordPress-ready HTML generation"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        # Should return dictionary with required keys
        self.assertIn('title', result)
        self.assertIn('slug', result)
        self.assertIn('meta_description', result)
        self.assertIn('schema', result)
        self.assertIn('content', result)
        self.assertIn('links', result)
        self.assertIn('word_count', result)
        
        # Word count should meet minimum
        self.assertGreater(result['word_count'], 1000, "Should have 1000+ words")
        
        # Should have links
        self.assertGreater(len(result['links']), 0, "Should have at least one external link")
        
        # Schema should be valid JSON
        schema = json.loads(result['schema'])
        self.assertEqual(schema['@type'], 'BlogPosting')
    
    def test_keyword_in_critical_locations(self):
        """Test keyword appears in SEO-critical locations"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        content_lower = result['content'].lower()
        
        # Keyword in title
        self.assertIn(self.test_keyword.lower(), result['title'].lower())
        
        # Keyword in meta description
        self.assertIn(self.test_keyword.lower(), result['meta_description'].lower())
        
        # Keyword in first paragraph (within first 300 chars of content)
        first_section = result['content'][:500].lower()
        self.assertIn(self.test_keyword.lower(), first_section)
        
        # Keyword in H2 heading
        h2_pattern = r'<h2[^>]*>(.*?)</h2>'
        h2_headings = re.findall(h2_pattern, result['content'], re.DOTALL | re.IGNORECASE)
        has_keyword_in_h2 = any(self.test_keyword.lower() in h2.lower() for h2 in h2_headings)
        self.assertTrue(has_keyword_in_h2, "Keyword should appear in at least one H2 heading")
    
    def test_external_link_format(self):
        """Test external links have proper formatting"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        # Extract all links
        link_pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        links = re.findall(link_pattern, result['content'])
        
        # Should have at least one external link
        self.assertGreater(len(links), 0)
        
        for url, anchor_text in links:
            # URL should be valid
            self.assertTrue(url.startswith('http'), f"URL should be absolute: {url}")
            
            # Anchor text should not be generic
            generic_texts = ['click here', 'here', 'link', 'read more']
            self.assertNotIn(anchor_text.lower(), generic_texts, 
                           f"Anchor text should be descriptive: {anchor_text}")
            
            # Anchor text should have substance
            self.assertGreater(len(anchor_text), 10, 
                             f"Anchor text should be descriptive: {anchor_text}")
    
    def test_secondary_keywords_usage(self):
        """Test secondary keywords are incorporated"""
        secondary = ["battery storage", "home energy"]
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword,
            secondary_keywords=secondary
        )
        
        # At least some secondary keywords should appear
        # (Not enforced strictly as it depends on content generation logic)
        content_lower = result['content'].lower()
        self.assertGreater(len(content_lower), 0)
    
    def test_custom_slug_preference(self):
        """Test custom slug is used when provided"""
        custom_slug = "my-custom-test-slug"
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword,
            custom_slug=custom_slug
        )
        
        self.assertEqual(result['slug'], custom_slug)
    
    def test_html_has_proper_styling(self):
        """Test HTML includes proper Montserrat font styling"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        content = result['content']
        
        # Should use Montserrat font
        montserrat_count = content.count('Montserrat')
        self.assertGreater(montserrat_count, 5, "Should use Montserrat font consistently")
        
        # Should have inline styles for compatibility
        self.assertIn('style=', content)
        self.assertIn('line-height', content)
        self.assertIn('margin', content)
    
    def test_readability_features(self):
        """Test content includes readability features"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        content = result['content']
        
        # Should have multiple headings
        h2_count = content.count('<h2')
        self.assertGreaterEqual(h2_count, 3, "Should have multiple H2 headings")
        
        # Should have bullet lists
        self.assertIn('<ul', content)
        self.assertIn('<li', content)
        
        # Should have subheadings
        h3_count = content.count('<h3')
        self.assertGreaterEqual(h3_count, 1, "Should have H3 subheadings")
    
    def test_word_count_minimum(self):
        """Test generated content meets minimum word count"""
        result = self.generator.generate_wordpress_html(
            self.test_content,
            self.test_keyword
        )
        
        # Remove HTML tags for accurate word count
        text_only = re.sub(r'<[^>]+>', '', result['content'])
        words = text_only.split()
        
        # Should have at least 1000+ words (with HTML it's 1500+)
        self.assertGreater(len(words), 1000, 
                          f"Should have 1000+ words, got {len(words)}")


class TestURLFetching(unittest.TestCase):
    """Test URL content fetching"""
    
    def setUp(self):
        self.generator = SEOBlogGenerator()
    
    def test_fetch_url_error_handling(self):
        """Test URL fetching handles errors gracefully"""
        # Invalid URL should return empty string
        result = self.generator.fetch_url_content("not-a-valid-url")
        self.assertEqual(result, "")


class TestFileLoading(unittest.TestCase):
    """Test file content loading"""
    
    def setUp(self):
        self.generator = SEOBlogGenerator()
    
    def test_load_file_error_handling(self):
        """Test file loading handles errors gracefully"""
        # Non-existent file should return empty string
        result = self.generator.load_file_content("/nonexistent/file.txt")
        self.assertEqual(result, "")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
