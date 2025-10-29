# 🚀 ST-ARC Quick Reference

## Start the Application

### Local (Development)
```bash
python app.py
```
Open: http://localhost:5000

### Docker (Production)
```bash
docker-compose up -d
```
Open: http://localhost:5000

## Using the Web Interface

### 1️⃣ Choose Input Method
- **📝 Text Input** - Paste reference content
- **🔗 URL** - Enter article URL
- **📄 File Upload** - Upload .txt, .html, or .md file

### 2️⃣ Fill Required Fields
- **Target Keyword** *(required)* - Your main SEO keyword
  - Example: `solar panel installation costs 2025`

### 3️⃣ Add Optional Fields
- **Secondary Keywords** - Related keywords (comma-separated)
  - Example: `solar costs, renewable energy, home solar`
- **URL Slug** - Custom URL (auto-generated if empty)
- **Chart Data** - Data for visualization
  - Format: `label1:value1,label2:value2`
  - Example: `2020:15,2021:23,2022:35`

### 4️⃣ Generate & Use
Click **Generate Blog Post**, then:
- 👁️ **Preview** - View HTML in new window
- 📋 **Copy** - Copy to clipboard
- ⬇️ **Download** - Save as .html file

## API Usage

### Generate Blog Post
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputMethod": "text",
    "content": "Your reference content here...",
    "keyword": "your target keyword",
    "secondaryKeywords": "keyword1, keyword2",
    "dataPoints": "2020:10,2021:20,2022:30"
  }'
```

### Health Check
```bash
curl http://localhost:5000/health
```

## Environment Variables

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
WP_APPLICATION_PASSWORD=your-wp-password  # Optional
WP_USERNAME=your-wp-username              # Optional
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Output Features

### Metadata
- ✅ SEO-optimized title
- ✅ URL-friendly slug
- ✅ Meta description (155-160 chars)
- ✅ Word count (1500+ words)

### Content
- ✅ H1, H2, H3 heading structure
- ✅ JSON-LD Schema markup
- ✅ Inline citations
- ✅ Data visualization
- ✅ Internal/external links
- ✅ WordPress-ready HTML

## Common Commands

### Development
```bash
# Start server
python app.py

# Run tests
python test_web_app.py
python test_seo_blog_generator.py

# Install dependencies
pip install -r requirements.txt
```

### Docker
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up -d --build
```

### Production
```bash
# With Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# Check health
curl http://localhost:5000/health
```

## Troubleshooting

### Port Already in Use
```bash
# Change port
FLASK_RUN_PORT=8080 python app.py
```

### File Upload Issues
- Max size: 16MB
- Formats: .txt, .html, .md
- Must be UTF-8 encoded

### Generation Fails
- Check internet connection (for URL fetching)
- Verify keyword is entered
- Check reference content is provided

## Keyboard Shortcuts

- **Ctrl/Cmd + Enter** - Submit form

## File Limits

- Max upload size: **16MB**
- Supported formats: **.txt, .html, .md**
- Min word count: **1500+ words** (output)

## Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Links

- 📖 [Full Documentation](README.md)
- 🌐 [Web Frontend Guide](WEB_FRONTEND_GUIDE.md)
- 🚀 [Deployment Guide](DEPLOYMENT.md)
- 🔒 [Security Review](SECURITY_REVIEW.md)
- 💻 [GitHub Repository](https://github.com/Burlyhodl/ST-ARC)

## Support

- Open an issue on GitHub
- Check logs for errors
- Review documentation
- Test health endpoint

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: 2025-10-29
