# 🚀 Deployment Guide

This guide covers deploying the AI-powered chatbot system to production environments.

## 📋 Pre-Deployment Checklist

- [ ] OpenAI API key configured
- [ ] Database properly seeded
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] CORS origins configured for your domain
- [ ] SSL certificate ready (for HTTPS)

## 🌐 Production Deployment Options

### Option 1: Traditional VPS/Server

#### Backend Deployment
```bash
# 1. Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip

# 2. Clone/upload your project
scp -r chatbot-system user@yourserver.com:/var/www/

# 3. Install dependencies
cd /var/www/chatbot-system/backend
pip3 install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your OpenAI API key

# 5. Initialize database
python3 init_db.py

# 6. Run with Gunicorn
pip3 install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### Frontend Deployment
```bash
# Serve with Nginx
sudo apt install nginx

# Copy frontend files to web root
sudo cp -r frontend/* /var/www/html/

# Configure Nginx (add to /etc/nginx/sites-available/default)
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /var/www/html;
        index index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

#### Docker Configuration

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM nginx:alpine

COPY . /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=sqlite:///./chatbot.db
    volumes:
      - ./backend/chatbot.db:/app/chatbot.db
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### Option 3: Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-chatbot-app

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here

# Deploy
git add .
git commit -m "Deploy chatbot"
git push heroku main
```

#### AWS/GCP/Azure
- Use their container services (ECS, Cloud Run, Container Instances)
- Upload Docker images to their registries
- Configure load balancers and auto-scaling

## 🔧 Production Configuration

### Backend Environment Variables
```env
# Required
OPENAI_API_KEY=your_actual_openai_key
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # For production DB

# Optional
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
MAX_SESSIONS=10000
SESSION_TIMEOUT=3600
```

### Frontend Configuration
Update `chatbot.js`:
```javascript
// Change API URL to your production backend
this.apiUrl = 'https://api.yourdomain.com';
```

### Database for Production
Switch from SQLite to PostgreSQL:

```python
# In database.py
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/chatbot")

# Install psycopg2
pip install psycopg2-binary
```

## 🔒 Security Considerations

### API Security
- Enable HTTPS only
- Configure CORS properly
- Add rate limiting
- Implement API authentication if needed

### Database Security
- Use environment variables for credentials
- Enable SSL connections
- Regular backups
- Access control

### Frontend Security
- Content Security Policy (CSP)
- XSS protection
- Secure cookies if using sessions

## 📊 Monitoring & Logging

### Backend Monitoring
```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

# Log conversations for analysis
@app.post("/chat")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    logging.info(f"Chat request: {message.session_id} - {message.message[:50]}...")
    # ... rest of function
```

### Performance Monitoring
- Use tools like New Relic, DataDog, or Prometheus
- Monitor API response times
- Track database query performance
- Set up alerts for errors

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Chatbot

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python -m pytest tests/
    
    - name: Deploy to production
      run: |
        # Your deployment commands here
        echo "Deploying to production..."
```

## 💾 Backup Strategy

### Database Backups
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sqlite3 chatbot.db ".dump" > backups/chatbot_$DATE.sql

# Keep only last 7 days
find backups/ -name "chatbot_*.sql" -mtime +7 -delete
```

### Configuration Backups
- Version control all configuration files
- Store environment variables securely
- Document deployment procedures

## 🚀 Scaling Considerations

### Horizontal Scaling
- Use load balancer for multiple backend instances
- Implement session stickiness or shared session storage
- Scale database (read replicas, sharding)

### Performance Optimization
- Add Redis for session caching
- Implement connection pooling
- Use CDN for frontend assets
- Enable gzip compression

## 📱 Mobile Optimization

### Progressive Web App (PWA)
Add to frontend:
```html
<!-- manifest.json -->
{
  "name": "AI Chatbot",
  "short_name": "Chatbot",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#667eea"
}

<!-- Service worker for offline capability -->
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
</script>
```

## 🔍 Health Checks

### Backend Health Endpoint
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Frontend Health Check
```javascript
// Add to chatbot.js
async checkHealth() {
    try {
        const response = await fetch(`${this.apiUrl}/health`);
        return response.ok;
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}
```

## 📈 Analytics Integration

### Track User Interactions
```javascript
// Google Analytics example
function trackChatInteraction(action, label) {
    gtag('event', action, {
        'event_category': 'Chatbot',
        'event_label': label
    });
}

// Call in chatbot.js
trackChatInteraction('message_sent', 'user_query');
trackChatInteraction('product_recommended', product.category);
```

## 🆘 Troubleshooting Production Issues

### Common Problems
1. **CORS errors**: Check allowed origins
2. **Database timeouts**: Increase connection limits
3. **High memory usage**: Implement session cleanup
4. **API rate limits**: Add request throttling

### Debug Tools
- Server logs: `tail -f /var/log/nginx/error.log`
- Application logs: `tail -f chatbot.log`
- Database monitoring: Connection counts, query times
- API monitoring: Response times, error rates
