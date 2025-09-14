# 🚀 UpShiftRx API Deployment Guide

## Quick Deploy Options

### 1. Railway (Recommended - Free tier)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```
**URL**: Auto-generated (e.g., `upshiftrx-api-production.up.railway.app`)

### 2. Render (Free tier)
1. Connect GitHub repo to Render
2. Select "Web Service"
3. Use existing `render.yaml` config
**URL**: Auto-generated

### 3. Vercel (Serverless)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```
**URL**: Auto-generated

### 4. Docker (Any platform)
```bash
# Build and run locally
docker build -t upshiftrx-api .
docker run -p 8000:8000 upshiftrx-api

# Deploy to any Docker platform (AWS ECS, Google Cloud Run, etc.)
```

## Environment Variables
Set these in your deployment platform:
- `PUBMED_EMAIL=contact@upshiftrx.ai`

## Test Deployment
```bash
curl https://your-api-url.com/health
```

## Best Choice: Railway
- ✅ Free tier with good limits
- ✅ Auto-deploys from GitHub
- ✅ Built-in monitoring
- ✅ Easy custom domains