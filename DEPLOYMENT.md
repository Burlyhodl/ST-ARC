# ST-ARC Web Frontend Deployment Guide

This guide provides instructions for deploying the ST-ARC Blog Post Generator web application to production.

## 🚀 Quick Start (Development)

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Development Server**
   ```bash
   python app.py
   ```

3. **Access the Application**
   Open your browser to: `http://localhost:5000`

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed (optional but recommended)

### Using Docker Compose (Easiest)

1. **Create Environment File**
   ```bash
   cp .env.example .env
   # Edit .env with your secret key
   ```

2. **Build and Run**
   ```bash
   docker-compose up -d
   ```

3. **Check Status**
   ```bash
   docker-compose ps
   docker-compose logs -f web
   ```

4. **Stop Application**
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build Image**
   ```bash
   docker build -t st-arc-generator .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name st-arc \
     -p 5000:5000 \
     -e SECRET_KEY="your-secret-key-here" \
     st-arc-generator
   ```

3. **Check Logs**
   ```bash
   docker logs -f st-arc
   ```

## ☁️ Cloud Platform Deployment

### Heroku

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   # or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile**
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set SECRET_KEY="your-secret-key"
   git push heroku main
   ```

### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init -p python-3.11 st-arc-generator
   ```

3. **Create Environment**
   ```bash
   eb create production
   eb setenv SECRET_KEY="your-secret-key"
   ```

4. **Deploy Updates**
   ```bash
   eb deploy
   ```

### Google Cloud Run

1. **Install gcloud CLI**

2. **Build and Deploy**
   ```bash
   gcloud run deploy st-arc-generator \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars SECRET_KEY="your-secret-key"
   ```

### DigitalOcean App Platform

1. **Create app.yaml**
   ```yaml
   name: st-arc-generator
   services:
   - name: web
     github:
       repo: Burlyhodl/ST-ARC
       branch: main
     dockerfile_path: Dockerfile
     http_port: 5000
     envs:
     - key: SECRET_KEY
       value: your-secret-key
   ```

2. **Deploy via Dashboard**
   - Go to DigitalOcean App Platform
   - Create new app
   - Connect GitHub repository
   - Deploy

## 🖥️ Traditional Server Deployment

### Using Nginx + Gunicorn (Ubuntu/Debian)

1. **Install System Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx supervisor
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/Burlyhodl/ST-ARC.git
   cd ST-ARC
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt gunicorn
   ```

4. **Create Environment File**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Configure Gunicorn (Supervisor)**
   Create `/etc/supervisor/conf.d/st-arc.conf`:
   ```ini
   [program:st-arc]
   directory=/path/to/ST-ARC
   command=/path/to/ST-ARC/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 app:app
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true
   environment=SECRET_KEY="your-secret-key"
   ```

6. **Configure Nginx**
   Create `/etc/nginx/sites-available/st-arc`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       client_max_body_size 16M;
   }
   ```

7. **Enable and Start Services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/st-arc /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start st-arc
   ```

8. **Setup SSL with Let's Encrypt (Optional)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## 🔒 Security Considerations

### Production Checklist

- [ ] Set a strong `SECRET_KEY` environment variable
- [ ] Use HTTPS/SSL in production
- [ ] Set `FLASK_ENV=production`
- [ ] Configure firewall rules
- [ ] Enable rate limiting (if needed)
- [ ] Regular security updates
- [ ] Monitor application logs
- [ ] Backup configuration and data

### Environment Variables

Required:
- `SECRET_KEY`: Cryptographic key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

Optional:
- `FLASK_ENV`: Set to `production` in production
- `WP_APPLICATION_PASSWORD`: For WordPress integration
- `WP_USERNAME`: WordPress username
- `WP_BASE_URL`: WordPress site URL

## 📊 Monitoring

### Health Check Endpoint

The application includes a health check endpoint:
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "ST-ARC Blog Generator",
  "version": "1.0.0"
}
```

### Logging

Logs are written to stdout by default. Configure log aggregation based on your platform:

- **Docker**: `docker logs <container-name>`
- **Heroku**: `heroku logs --tail`
- **Server**: Check supervisor or systemd logs

## 🔧 Troubleshooting

### Application Won't Start

1. Check Python version (requires 3.6+)
   ```bash
   python --version
   ```

2. Verify all dependencies are installed
   ```bash
   pip list
   ```

3. Check environment variables
   ```bash
   echo $SECRET_KEY
   ```

### Port Already in Use

Change the port in docker-compose.yml or when running:
```bash
# Docker
docker run -p 8080:5000 st-arc-generator

# Direct
python app.py  # Edit app.py to change port
```

### File Upload Issues

- Check `MAX_CONTENT_LENGTH` setting (default 16MB)
- Verify file permissions
- Check available disk space

### Generation Timeouts

- Increase Gunicorn timeout: `--timeout 120`
- Check network connectivity for URL fetching
- Monitor resource usage (CPU/Memory)

## 📈 Scaling

### Horizontal Scaling

Increase number of workers:
```bash
gunicorn --workers 8 app:app
```

### Load Balancing

Use Nginx or cloud load balancer to distribute traffic across multiple instances.

### Caching

Consider adding Redis for caching frequently generated content (future enhancement).

## 🔄 Updates and Maintenance

### Updating the Application

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

2. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Restart Application**
   ```bash
   # Docker Compose
   docker-compose restart
   
   # Supervisor
   sudo supervisorctl restart st-arc
   
   # Systemd
   sudo systemctl restart st-arc
   ```

### Backup

Important files to backup:
- `.env` (environment configuration)
- Custom templates (if modified)
- Application logs

## 📞 Support

For deployment issues:
1. Check the application logs
2. Verify environment variables
3. Test the health endpoint
4. Review this documentation
5. Open an issue on GitHub

## 📝 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**Production Status:** ✅ Ready for deployment

For more information, see the main README.md
