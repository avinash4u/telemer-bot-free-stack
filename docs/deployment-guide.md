# TeleMER Bot - Public Deployment Guide

## Overview

This guide explains how to deploy the TeleMER WebRTC frontend for public access. The WebRTC interface provides a browser-based medical consultation interface with AI-powered medical coding and family member tracking.

## Quick Start

### 1. Start WebRTC Server

```bash
# Navigate to project directory
cd /Users/avinash.kumar/Downloads/telemer-bot-free-stack

# Start WebRTC server with public access
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

### 2. Access the Interface

**Local Access:**
```
http://localhost:3001
```

**Public Access:**
Replace `localhost` with your server's public IP address:
```
http://YOUR_PUBLIC_IP:3001
```

## Deployment Options

### Option 1: Local Development (Current Setup)

**Configuration:** `docker-compose.webrtc-simple.yml`

**Features:**
- ✅ WebRTC frontend with nginx
- ✅ Public IP binding (0.0.0.0:3001)
- ✅ Family member tracking
- ✅ Medical coding with ICD-10
- ✅ Intelligent call ending
- ✅ Real-time speech recognition

**Access:** `http://localhost:3001`

### Option 2: Cloud Deployment

#### AWS EC2 Deployment

1. **Launch EC2 Instance:**
```bash
# Ubuntu 20.04 LTS, t2.micro (Free Tier)
# Security Group: Allow HTTP (80), HTTPS (443), Custom (3001)
```

2. **Deploy Application:**
```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Clone repository
git clone https://github.com/avinash4u/telemer-bot-free-stack.git
cd telemer-bot-free-stack

# Start WebRTC server
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

3. **Access:** `http://your-ec2-ip:3001`

#### Google Cloud Platform

1. **Create VM Instance:**
```bash
# Compute Engine > VM Instances > Create
# Machine type: e2-micro (Free Tier)
# Firewall: Allow HTTP, HTTPS, Custom (3001)
```

2. **Deploy:**
```bash
# SSH into VM
gcloud compute ssh instance-name

# Clone and deploy
git clone https://github.com/avinash4u/telemer-bot-free-stack.git
cd telemer-bot-free-stack
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

#### DigitalOcean

1. **Create Droplet:**
```bash
# Ubuntu 20.04, Basic Plan ($5/month)
# Firewall: Allow HTTP, HTTPS, Custom (3001)
```

2. **Deploy:**
```bash
# SSH into Droplet
ssh root@your-droplet-ip

# Clone and deploy
git clone https://github.com/avinash4u/telemer-bot-free-stack.git
cd telemer-bot-free-stack
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

### Option 3: Domain with HTTPS

#### Using Nginx Reverse Proxy

1. **Create nginx configuration:**
```nginx
# /etc/nginx/sites-available/telemer
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. **Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/telemer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

3. **Add SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

#### Using Cloudflare

1. **Sign up for Cloudflare account**
2. **Add your domain**
3. **Set DNS A record:** `yourdomain.com` → `YOUR_SERVER_IP`
4. **Enable SSL/TLS:** Flexible mode
5. **Access:** `https://yourdomain.com`

## Production Considerations

### Security

1. **Firewall Configuration:**
```bash
# Only allow necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw allow 3001  # WebRTC (if not using reverse proxy)
sudo ufw enable
```

2. **Docker Security:**
```bash
# Use non-root containers
# Regular updates
docker-compose pull
docker-compose up -d
```

3. **Environment Variables:**
```bash
# Set production environment
export NODE_ENV=production
export API_URL=https://your-api-domain.com
```

### Performance

1. **Enable Gzip Compression:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Browser Caching:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **CDN Integration:**
```yaml
# docker-compose.yml
services:
  webrtc-server:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./webrtc-client:/usr/share/nginx/html
```

### Monitoring

1. **Health Check:**
```bash
# Add to docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3001"]
  interval: 30s
  timeout: 10s
  retries: 3
```

2. **Logging:**
```bash
# View logs
docker-compose -f docker-compose.webrtc-simple.yml logs -f

# Log rotation
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Full Stack Deployment

### Complete System Deployment

For production deployment with all services:

1. **Start All Services:**
```bash
# Main orchestrator and AI services
docker-compose up -d

# WebRTC frontend
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

2. **Verify Services:**
```bash
# Check all containers
docker ps

# Test API endpoints
curl http://localhost:8000/health

# Test WebRTC interface
curl http://localhost:3001
```

### Service URLs

- **WebRTC Frontend:** `http://your-ip:3001`
- **API Health:** `http://your-ip:8000/health`
- **API Documentation:** `http://your-ip:8000/docs`

## Troubleshooting

### Common Issues

1. **Port Already in Use:**
```bash
# Check port usage
sudo netstat -tulpn | grep :3001

# Kill process
sudo kill -9 <PID>
```

2. **Docker Container Issues:**
```bash
# View logs
docker-compose -f docker-compose.webrtc-simple.yml logs

# Restart container
docker-compose -f docker-compose.webrtc-simple.yml restart
```

3. **Network Access Issues:**
```bash
# Check firewall
sudo ufw status

# Test connectivity
telnet your-ip 3001
```

4. **CORS Issues:**
```bash
# Check API CORS settings
curl -H "Origin: http://your-ip:3001" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS http://your-ip:8000/calls
```

### Debug Commands

```bash
# Check container status
docker ps -a

# Inspect container
docker inspect telemer-bot-free-stack-webrtc-server-1

# Access container shell
docker exec -it telemer-bot-free-stack-webrtc-server-1 sh

# Monitor real-time logs
docker-compose -f docker-compose.webrtc-simple.yml logs -f
```

## Performance Optimization

### Frontend Optimization

1. **Minimize Assets:**
```bash
# Add to nginx.conf
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Enable HTTP/2:**
```nginx
listen 443 ssl http2;
```

3. **Browser Caching:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Backend Optimization

1. **Database Connection Pooling:**
```python
# In app/core/db.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

2. **Redis Caching:**
```python
# Cache API responses
@cache.memoize(timeout=300)
def process_utterance(db, case, text):
    # Processing logic
```

## Scaling

### Horizontal Scaling

1. **Load Balancer Setup:**
```yaml
# docker-compose.scale.yml
services:
  webrtc-server:
    image: nginx:alpine
    deploy:
      replicas: 3
    ports:
      - "3001:80"
```

2. **Database Scaling:**
```bash
# Read replicas
# Connection pooling
# Query optimization
```

## Security Best Practices

1. **HTTPS Only:**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

2. **Security Headers:**
```nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

3. **Rate Limiting:**
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

## Conclusion

The TeleMER WebRTC interface can be deployed using various methods:

- **Local Development:** Quick setup with `docker-compose.webrtc-simple.yml`
- **Cloud Deployment:** AWS, GCP, DigitalOcean with public IP access
- **Production Setup:** Domain, HTTPS, reverse proxy, monitoring

The deployment provides:
- ✅ Public WebRTC access
- ✅ Medical coding with ICD-10
- ✅ Family member tracking
- ✅ Intelligent call ending
- ✅ Real-time speech recognition
- ✅ Secure, scalable architecture

Choose the deployment method that best fits your needs and follow the security and performance recommendations for production use.
