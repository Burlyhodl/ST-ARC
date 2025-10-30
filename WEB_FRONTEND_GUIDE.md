# ST-ARC Web Frontend - User Guide

## 🌐 Production-Ready Web Interface

ST-ARC now features a modern, user-friendly web interface that makes generating SEO-optimized blog posts easy for everyone - no coding required!

## ✨ Features

### User Experience
- 🎨 **Modern, Responsive Design** - Works beautifully on desktop, tablet, and mobile
- 🚀 **Real-time Generation** - See your blog post created instantly
- 📱 **Mobile-Friendly** - Full functionality on all devices
- ⚡ **Fast & Efficient** - Optimized for quick generation

### Input Options
- 📝 **Text Input** - Paste reference content directly
- 🔗 **URL Fetching** - Automatically extract content from any URL
- 📄 **File Upload** - Upload .txt, .html, or .md files (up to 16MB)

### Output Features
- 👁️ **Live Preview** - Preview HTML in new window
- 📋 **One-Click Copy** - Copy HTML to clipboard instantly
- ⬇️ **Download** - Save HTML file directly to your computer
- 📊 **Metadata Display** - See title, slug, meta description, and word count

## 🚀 Quick Start

### Option 1: Run Locally (Development)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

### Option 2: Docker (Production)

1. **Using Docker Compose (Recommended):**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   Navigate to `http://localhost:5000`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📖 How to Use

### Step 1: Choose Your Content Source

Select one of three input methods:
- **Text Input**: Paste reference content directly
- **URL**: Enter a URL to fetch content
- **File Upload**: Upload a text file with reference content

### Step 2: Enter Your Keyword

Enter your target SEO keyword (required):
```
Example: "Tesla Powerwall installation cost Arizona"
```

### Step 3: Add Optional Details

Enhance your blog post with:
- **Secondary Keywords**: Related keywords to incorporate naturally
- **Custom Slug**: Custom URL slug (or let it auto-generate)
- **Chart Data**: Data points for visualization (format: `label1:value1,label2:value2`)

### Step 4: Generate & Download

Click "Generate Blog Post" and wait a few seconds. Once complete:
- ✅ View metadata (title, slug, description, word count)
- 👁️ Preview the HTML in a new window
- 📋 Copy HTML to clipboard
- ⬇️ Download as .html file

## 🎯 Example Usage

### Basic Generation

1. Select **Text Input**
2. Paste:
   ```
   Solar panels are becoming increasingly popular as homeowners look 
   for ways to reduce energy costs and environmental impact.
   ```
3. Enter keyword: `residential solar panels 2025`
4. Click **Generate Blog Post**

### With Data Visualization

1. Enter your content and keyword as usual
2. Add chart data:
   ```
   2020:15,2021:23,2022:35,2023:48,2024:62
   ```
3. Generate and see an interactive chart in your blog post!

## 🔧 Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```bash
# Required for production
SECRET_KEY=your-secret-key-here

# Optional
FLASK_ENV=production
WP_APPLICATION_PASSWORD=your-wp-password
WP_USERNAME=your-wp-username
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🔒 Security Features

- ✅ CSRF protection
- ✅ File size limits (16MB max)
- ✅ Input validation
- ✅ Secure headers
- ✅ Environment-based configuration

## 📱 Screenshots

### Homepage
![ST-ARC Homepage](https://github.com/user-attachments/assets/e08c4fc7-8410-4019-8226-6f377f83bdcb)

### Results Page
![ST-ARC Results](https://github.com/user-attachments/assets/d4bb153e-480c-4440-b042-5146b1f4e977)

## 🎨 Customization

### Branding

Edit `/templates/index.html` to customize:
- Logo and header
- Color scheme
- Feature highlights

### Styling

Edit `/static/css/style.css` to modify:
- Colors (CSS variables at top)
- Layout and spacing
- Mobile breakpoints

### API

The web app uses a RESTful API. Endpoints:

- `POST /api/generate` - Generate blog post
- `POST /api/upload` - Upload file
- `POST /api/download` - Download HTML
- `GET /health` - Health check

## 🌐 API Usage

You can also use the API directly:

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputMethod": "text",
    "content": "Your reference content here",
    "keyword": "your target keyword",
    "secondaryKeywords": "keyword1, keyword2",
    "slug": "custom-slug",
    "dataPoints": "2020:10,2021:20,2022:30"
  }'
```

## 🚀 Production Deployment

For production deployment options including:
- Docker/Docker Compose
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- DigitalOcean App Platform
- Traditional server with Nginx

See the comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) guide.

## 💡 Tips & Best Practices

### For Best Results

1. **Provide Quality Content**: Use authoritative reference material
2. **Specific Keywords**: Use specific, realistic keywords (not too broad)
3. **Review Output**: Always review generated content before publishing
4. **Customize**: Edit the HTML to match your exact needs

### Performance

- Generation typically takes 2-5 seconds
- File uploads are processed immediately
- URL fetching depends on source website speed

## 🔄 From CLI to Web

If you previously used the CLI version:

**Old way (CLI):**
```bash
python seo_blog_generator.py
# Follow prompts...
```

**New way (Web):**
1. Open browser to `http://localhost:5000`
2. Fill form
3. Click generate
4. Download result

The web interface provides the same powerful generation with a much better UX!

## 🆘 Troubleshooting

### Server Won't Start

**Error: "Port 5000 is in use"**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
FLASK_RUN_PORT=8080 python app.py
```

### Generation Fails

- Check your internet connection (for URL fetching)
- Verify input content is provided
- Ensure keyword is entered
- Check server logs for errors

### File Upload Issues

- Maximum file size: 16MB
- Supported formats: .txt, .html, .md
- Ensure file is UTF-8 encoded

## 📞 Support

For issues or questions:
1. Check the logs: `docker-compose logs -f` or check console
2. Review [DEPLOYMENT.md](DEPLOYMENT.md)
3. Open an issue on GitHub

## 🎓 Next Steps

1. ✅ Start the web server
2. ✅ Generate your first blog post
3. ✅ Customize the branding (optional)
4. ✅ Deploy to production
5. ✅ Share with your team!

---

**Production Ready** ✅ | **Mobile Responsive** ✅ | **Secure** ✅ | **Fast** ✅

For more information, see the main [README.md](README.md)
