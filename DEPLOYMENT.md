# TripStar AI - Deployment Guide

This guide covers deploying TripStar AI to various hosting platforms.

## 📋 Pre-Deployment Checklist

- [ ] Gemini API key is ready
- [ ] All dependencies are in `requirements.txt`
- [ ] Debug mode is disabled for production
- [ ] `.env` file is in `.gitignore`
- [ ] Application tested locally

## 🚀 Deployment Options

### 1. Heroku (Easy, Free Tier Available)

#### Step 1: Prepare Your Application

Create a `Procfile` in your project root:
```
web: gunicorn app:app
```

Add `gunicorn` to `requirements.txt`:
```
gunicorn==21.2.0
```

Update `app.py` for production:
```python
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

#### Step 2: Deploy to Heroku

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create tripstar-ai

# Set environment variables
heroku config:set GEMINI_API_KEY=your_api_key_here

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Open your app
heroku open
```

---

### 2. Render (Easy, Free Tier Available)

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

#### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: tripstar-ai
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: your_api_key
6. Click "Create Web Service"

---

### 3. Railway (Very Easy, Free Tier Available)

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

#### Step 2: Deploy on Railway

1. Go to [Railway](https://railway.app/)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add Environment Variable:
   - **Variable**: `GEMINI_API_KEY`
   - **Value**: your_api_key
6. Railway auto-detects Flask and deploys

---

### 4. PythonAnywhere (Easy, Free Tier Available)

#### Step 1: Upload Files

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Go to "Files" tab
3. Upload all your files

#### Step 2: Create Virtual Environment

Open a Bash console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 tripstar-venv
pip install -r requirements.txt
```

#### Step 3: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Choose Python 3.10
5. Set source code path: `/home/yourusername/tripstar-ai`
6. Set virtualenv path: `/home/yourusername/.virtualenvs/tripstar-venv`

#### Step 4: Edit WSGI File

```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/tripstar-ai'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'

from app import app as application
```

---

### 5. Google Cloud Run (Scalable, Pay-as-you-go)

#### Step 1: Create Dockerfile

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

#### Step 2: Deploy to Cloud Run

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Initialize gcloud
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy tripstar-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here
```

---

### 6. DigitalOcean App Platform

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

#### Step 2: Deploy on DigitalOcean

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Configure:
   - **Type**: Web Service
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn --worker-tmp-dir /dev/shm app:app`
5. Add Environment Variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: your_api_key
6. Click "Create Resources"

---

### 7. AWS Elastic Beanstalk

#### Step 1: Create requirements.txt

Ensure gunicorn is included:
```
Flask==3.0.0
google-generativeai==0.3.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

#### Step 2: Create .ebextensions

Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    GEMINI_API_KEY: your_api_key_here
```

#### Step 3: Deploy

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 tripstar-ai

# Create environment and deploy
eb create tripstar-env
eb deploy

# Open application
eb open
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
✅ **DO**: Store API keys in environment variables
❌ **DON'T**: Hardcode API keys in source code

### 2. HTTPS
✅ **DO**: Use HTTPS in production (most platforms provide this automatically)
❌ **DON'T**: Use HTTP for sensitive data

### 3. Rate Limiting
Add rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 4. CORS (if needed)
If you plan to build a separate frontend:

```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app)
```

### 5. Production Settings

Update `app.py`:
```python
if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'production')
    debug = env == 'development'
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)
```

---

## 📊 Monitoring & Analytics

### 1. Error Tracking (Sentry)

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
)
```

### 2. Application Monitoring

Most platforms provide built-in monitoring:
- **Heroku**: Heroku Metrics
- **Render**: Built-in metrics dashboard
- **Railway**: Resource usage graphs
- **Google Cloud**: Cloud Monitoring

---

## 🎯 Performance Optimization

### 1. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/generate-itinerary', methods=['POST'])
@cache.cached(timeout=300, key_prefix='itinerary')
def generate_itinerary():
    # ... existing code
```

### 2. Optimize Gemini Requests

```python
# Use streaming for faster responses
response = model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.8,
        max_output_tokens=3000,
    ),
    stream=True
)
```

### 3. Compress Responses

```bash
pip install flask-compress
```

```python
from flask_compress import Compress
Compress(app)
```

---

## 🐛 Troubleshooting

### Application Won't Start
1. Check logs on your platform
2. Verify all environment variables are set
3. Ensure `gunicorn` is in requirements.txt
4. Check Python version compatibility

### API Errors
1. Verify Gemini API key is correct
2. Check API quota/limits
3. Review error logs for specific messages

### Slow Response Times
1. Increase worker count in gunicorn
2. Consider using async workers
3. Implement caching
4. Optimize Gemini API calls

---

## 📞 Platform Support

- **Heroku**: [Help Center](https://help.heroku.com/)
- **Render**: [Documentation](https://render.com/docs)
- **Railway**: [Discord Community](https://discord.gg/railway)
- **PythonAnywhere**: [Forums](https://www.pythonanywhere.com/forums/)
- **Google Cloud**: [Support](https://cloud.google.com/support)

---

## ✅ Post-Deployment Checklist

- [ ] Application is accessible via HTTPS
- [ ] Environment variables are properly set
- [ ] Error tracking is configured
- [ ] Rate limiting is enabled
- [ ] Application logs are monitored
- [ ] Backup strategy is in place
- [ ] Custom domain is configured (if applicable)

---

**Happy Deploying! 🚀**