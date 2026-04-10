# Vercel Deployment Guide for TeleMER Bot

## Overview

Vercel provides a free, fast way to deploy the TeleMER Bot frontend with a public URL. This setup creates a serverless API proxy to connect the Vercel frontend to your local backend services.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vercel CDN    │    │  Vercel Edge   │    │ Local Services  │
│                 │    │   Functions     │    │                 │
│  Frontend       │    │                 │    │  Orchestrator   │
│  (Static)       │    │  API Proxy      │    │  Port 8000     │
│                 │    │                 │    │                 │
│  Public URL     │    │                 │    │  WebRTC        │
│                 │    │                 │    │  Port 3001     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### 1. Automated Setup
```bash
# Run the setup script
./scripts/setup-vercel.sh

# Choose deployment type:
# 1. Production (vercel.com)
# 2. Preview (vercel.app)
# 3. Local development
```

### 2. Manual Setup
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to production
vercel --prod

# Or deploy to preview
vercel
```

## Deployment Options

### Option 1: Production Deployment
**URL:** `https://telemer-bot.vercel.app`

**Features:**
- ✅ Permanent public URL
- ✅ Global CDN distribution
- ✅ SSL/HTTPS included
- ✅ Custom domain support
- ✅ Analytics and logs

**Setup:**
```bash
vercel --prod
```

### Option 2: Preview Deployment
**URL:** `https://telemer-bot-[random].vercel.app`

**Features:**
- ✅ Temporary URL for testing
- ✅ Instant deployment
- ✅ Shareable for feedback
- ✅ Automatic cleanup

**Setup:**
```bash
vercel
```

### Option 3: Local Development
**URL:** `http://localhost:3000`

**Features:**
- ✅ Hot reload
- ✅ Local API proxy
- ✅ Development tools
- ✅ Fast iteration

**Setup:**
```bash
vercel dev
```

## Configuration Files

### vercel.json
```json
{
  "version": 2,
  "name": "telemer-bot",
  "builds": [
    {
      "src": "webrtc-client/index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/webrtc-client/$1"
    }
  ],
  "functions": {
    "api/calls.js": {
      "maxDuration": 30
    }
  }
}
```

### package.json
```json
{
  "name": "telemer-bot",
  "version": "1.0.0",
  "scripts": {
    "dev": "vercel dev",
    "build": "vercel build",
    "deploy": "vercel --prod"
  },
  "dependencies": {
    "node-fetch": "^2.6.7"
  }
}
```

### API Proxy (api/calls.js)
```javascript
// Proxies /api/* requests to local orchestrator
const ORCHESTRATOR_URL = process.env.ORCHESTRATOR_URL || 'http://localhost:8000';

// Handles CORS and forwards requests
module.exports = async (req, res) => {
  if (path.startsWith('/calls/')) {
    const response = await fetch(`${ORCHESTRATOR_URL}${path}${search}`);
    // Forward response with CORS headers
    return res.end(data);
  }
};
```

## URL Structure

### Production URLs
```
Frontend: https://telemer-bot.vercel.app
API Proxy: https://telemer-bot.vercel.app/api/calls/*
Health Check: https://telemer-bot.vercel.app/api/health
```

### Preview URLs
```
Frontend: https://telemer-bot-abc123.vercel.app
API Proxy: https://telemer-bot-abc123.vercel.app/api/calls/*
```

## Local Services Setup

### Required Services
```bash
# Start all services
docker-compose up -d

# Start only orchestrator
docker-compose up -d orchestrator

# Start WebRTC (for local testing)
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

### Service URLs
```
Orchestrator: http://localhost:8000
WebRTC: http://localhost:3001
API Health: http://localhost:8000/health
```

## API Integration

### Frontend Configuration
The Vercel frontend automatically proxies API calls to your local orchestrator:

```javascript
// In webrtc-client/index.html
const API_BASE = window.location.origin; // Uses Vercel domain

// API calls are proxied to local orchestrator
fetch(`${API_BASE}/api/calls/${caseId}/utterance`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text, session_id })
});
```

### Environment Variables
```bash
# Set orchestrator URL (optional)
export ORCHESTRATOR_URL=http://localhost:8000

# Deploy with custom backend
vercel --prod
```

## Custom Domain Setup

### Step 1: Deploy to Vercel
```bash
vercel --prod
```

### Step 2: Add Custom Domain
1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Domains
4. Add your domain: `telemer.health`
5. Configure DNS records

### Step 3: DNS Configuration
```
Type: CNAME
Name: telemer (or @)
Value: cname.vercel-dns.com
TTL: 300
```

## SSL and Security

### Automatic SSL
- ✅ SSL certificate provided by Vercel
- ✅ Automatic renewal
- ✅ HTTP to HTTPS redirect
- ✅ Security headers included

### Security Headers
```javascript
// Added by API proxy
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type,Authorization'
};
```

## Performance

### CDN Distribution
- ✅ Global edge locations
- ✅ Automatic caching
- ✅ Image optimization
- ✅ Compression enabled

### Caching Strategy
```javascript
// Static assets cached by Vercel
// API responses cached based on headers
// Medical data not cached (real-time required)
```

## Monitoring and Analytics

### Vercel Analytics
```bash
# View deployment metrics
vercel ls

# View real-time logs
vercel logs

# View function invocations
vercel logs --filter="/api/calls"
```

### Custom Monitoring
```javascript
// Add to frontend
console.log('Medical analysis:', { symptoms, codes, timestamp });

// Add to API proxy
console.log('API request:', { path, method, response_time });
```

## Troubleshooting

### Common Issues

**1. API Calls Failing**
```bash
# Check local orchestrator
curl http://localhost:8000/health

# Check Vercel logs
vercel logs

# Test API proxy directly
curl https://telemer-bot.vercel.app/api/health
```

**2. CORS Issues**
```bash
# Check CORS headers in API proxy
curl -H "Origin: https://telemer-bot.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://telemer-bot.vercel.app/api/calls
```

**3. Deployment Failures**
```bash
# Check vercel.json syntax
vercel build

# Check package.json dependencies
npm install

# Clear Vercel cache
rm -rf .vercel
vercel --prod
```

### Debug Mode
```bash
# Deploy with debug logs
DEBUG=* vercel --prod

# Local development with debug
vercel dev --debug
```

## Advanced Configuration

### Custom API Routes
```json
// vercel.json
{
  "routes": [
    {
      "src": "/api/health",
      "dest": "/api/calls.js"
    },
    {
      "src": "/api/calls/(.*)",
      "dest": "/api/calls.js"
    }
  ]
}
```

### Environment-Specific Config
```json
// vercel.json
{
  "env": {
    "ORCHESTRATOR_URL": "@orchestrator-url"
  }
}
```

### Function Configuration
```json
{
  "functions": {
    "api/calls.js": {
      "maxDuration": 30,
      "memory": 512,
      "runtime": "nodejs18.x"
    }
  }
}
```

## Best Practices

### Performance
1. **Optimize API responses**
   - Use appropriate HTTP status codes
   - Minimize response size
   - Enable compression

2. **Frontend optimization**
   - Lazy load components
   - Optimize images
   - Use efficient JavaScript

3. **Caching strategy**
   - Cache static assets
   - Don't cache medical data
   - Use appropriate TTL

### Security
1. **API security**
   - Validate input data
   - Rate limiting
   - Authentication for sensitive data

2. **Frontend security**
   - HTTPS only
   - Security headers
   - Input sanitization

### Deployment
1. **CI/CD integration**
   - GitHub Actions
   - Automated testing
   - Staged deployments

2. **Rollback strategy**
   - Keep previous deployments
   - Quick rollback capability
   - Health checks

## Cost and Limits

### Vercel Free Tier
- ✅ 100GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Custom domains
- ✅ Serverless functions
- ✅ Edge network

### Usage Monitoring
```bash
# Check bandwidth usage
vercel ls

# Monitor function invocations
vercel logs --limit=100

# Set up alerts (Vercel Dashboard)
```

## Conclusion

Vercel deployment provides:
- ✅ **Free public URL** - No hosting costs
- ✅ **Global CDN** - Fast worldwide access
- ✅ **SSL/HTTPS** - Secure connections
- ✅ **API proxy** - Connects to local services
- ✅ **Easy deployment** - One-command deployment

**Your TeleMER Bot gets a professional public URL with Vercel's enterprise-grade infrastructure!**

### Next Steps
1. Run `./scripts/setup-vercel.sh`
2. Choose deployment type
3. Test medical features at public URL
4. Share with users and stakeholders

### Alternative: Local Development
If Vercel deployment isn't needed, use:
- `http://telemer.local` (local domain)
- `http://localhost:3001` (direct access)
- Cloudflare tunnel for external access

Choose the deployment method that best fits your requirements!
