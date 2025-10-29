#!/usr/bin/env python3
"""
Flask Web Application for ST-ARC Blog Post Generator
Production-ready web interface for public use
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from seo_blog_generator import SEOBlogGenerator

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize generator
generator = SEOBlogGenerator()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_blog():
    """Generate blog post from user input"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('keyword'):
            return jsonify({'error': 'Keyword is required'}), 400
        
        # Get input content
        input_content = ""
        input_method = data.get('inputMethod', 'text')
        
        if input_method == 'url':
            url = data.get('url', '').strip()
            if not url:
                return jsonify({'error': 'URL is required'}), 400
            input_content = generator.fetch_url_content(url)
            if not input_content:
                return jsonify({'error': 'Failed to fetch content from URL'}), 400
                
        elif input_method == 'text':
            input_content = data.get('content', '').strip()
            if not input_content:
                return jsonify({'error': 'Content is required'}), 400
                
        elif input_method == 'file':
            # File upload handled separately via multipart/form-data
            return jsonify({'error': 'File upload should use the /api/upload endpoint'}), 400
        
        # Extract parameters
        keyword = data.get('keyword', '').strip()
        secondary_keywords = [k.strip() for k in data.get('secondaryKeywords', '').split(',') if k.strip()]
        custom_slug = data.get('slug', '').strip()
        
        # Parse data points if provided
        data_points = None
        data_input = data.get('dataPoints', '').strip()
        if data_input:
            try:
                # Format: label1:value1,label2:value2
                pairs = [p.strip() for p in data_input.split(',') if p.strip()]
                labels = []
                values = []
                for pair in pairs:
                    if ':' in pair:
                        label, value = pair.split(':', 1)
                        labels.append(label.strip())
                        values.append(float(value.strip()))
                
                if labels and values:
                    data_points = {
                        'labels': labels,
                        'values': values,
                        'title': f'{keyword} Data Visualization'
                    }
            except Exception as e:
                # If data parsing fails, just skip visualization
                print(f"Warning: Failed to parse data points: {e}")
        
        # Generate the blog post
        result = generator.generate_wordpress_html(
            input_content=input_content,
            keyword=keyword,
            secondary_keywords=secondary_keywords if secondary_keywords else None,
            custom_slug=custom_slug if custom_slug else None,
            data_points=data_points
        )
        
        # Add generation timestamp
        result['generated_at'] = datetime.now().isoformat()
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error generating blog post: {e}")
        return jsonify({'error': f'Failed to generate blog post: {str(e)}'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload for content input"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        
        return jsonify({'content': content}), 200
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download_html():
    """Download generated HTML as file"""
    try:
        data = request.get_json()
        html_content = data.get('html', '')
        filename = data.get('filename', 'blog_post.html')
        
        if not html_content:
            return jsonify({'error': 'No content to download'}), 400
        
        # Create a BytesIO object
        buffer = BytesIO()
        buffer.write(html_content.encode('utf-8'))
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ST-ARC Blog Generator',
        'version': '1.0.0'
    }), 200

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
