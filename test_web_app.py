#!/usr/bin/env python3
"""
Tests for ST-ARC Web Application
"""

import unittest
import json
from app import app

class TestWebApp(unittest.TestCase):
    """Test cases for the web application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_page(self):
        """Test that index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ST-ARC', response.data)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'ST-ARC Blog Generator')
    
    def test_generate_blog_missing_keyword(self):
        """Test blog generation fails without keyword"""
        response = self.client.post('/api/generate',
            data=json.dumps({
                'inputMethod': 'text',
                'content': 'Test content'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_blog_missing_content(self):
        """Test blog generation fails without content"""
        response = self.client.post('/api/generate',
            data=json.dumps({
                'inputMethod': 'text',
                'keyword': 'test keyword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_blog_success(self):
        """Test successful blog generation"""
        response = self.client.post('/api/generate',
            data=json.dumps({
                'inputMethod': 'text',
                'content': 'Solar panels are a great way to save money and reduce environmental impact. They have become more affordable in recent years.',
                'keyword': 'residential solar panels',
                'secondaryKeywords': 'solar energy, home solar'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check required fields
        self.assertIn('title', data)
        self.assertIn('slug', data)
        self.assertIn('meta_description', data)
        self.assertIn('content', data)
        self.assertIn('word_count', data)
        
        # Verify content quality
        self.assertGreaterEqual(data['word_count'], 1500)
        self.assertIn('residential solar panels', data['title'].lower())
    
    def test_generate_blog_with_slug(self):
        """Test blog generation with custom slug"""
        response = self.client.post('/api/generate',
            data=json.dumps({
                'inputMethod': 'text',
                'content': 'Test content about solar energy.',
                'keyword': 'solar energy',
                'slug': 'my-custom-slug'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['slug'], 'my-custom-slug')
    
    def test_invalid_endpoint(self):
        """Test 404 for invalid endpoint"""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
    
    def test_download_missing_content(self):
        """Test download fails without content"""
        response = self.client.post('/api/download',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(verbosity=2)
