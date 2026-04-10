# User-Friendly URLs for TeleMER Bot

## Overview

The TeleMER Bot can be accessed with user-friendly domain names instead of IP addresses. This guide shows you how to set up various options for easy access.

## Quick Setup Options

### Option 1: Local Domain (Easiest)

**Setup:** `./scripts/setup-friendly-url.sh` → Choose option 1

**URL:** `http://telemer.local`

**Features:**
- ✅ No external dependencies
- ✅ Works immediately
- ✅ Professional appearance
- ✅ Easy to remember

**Setup Commands:**
```bash
# Run the setup script
./scripts/setup-friendly-url.sh

# Choose option 1 for local domain
# The script will:
# 1. Configure nginx for telemer.local
# 2. Add entry to hosts file
# 3. Start the service
```

**Manual Setup:**
```bash
# Add to /etc/hosts (system-wide) or ~/.hosts (user)
echo "127.0.0.1 telemer.local" >> /etc/hosts

# Start with public configuration
docker-compose -f docker-compose.public.yml up -d
```

### Option 2: Custom Domain

**Setup:** `./scripts/setup-friendly-url.sh` → Choose option 2

**URL:** `http://your-domain.com` (e.g., `http://telemer.health`)

**Features:**
- ✅ Professional domain name
- ✅ SSL support available
- ✅ Full control over branding
- ✅ Suitable for production

**Setup Commands:**
```bash
# Run the setup script
./scripts/setup-friendly-url.sh

# Choose option 2
# Enter your domain when prompted
# Configure DNS A record
```

**DNS Configuration:**
```
Type: A
Name: @ (or your subdomain)
Value: YOUR_PUBLIC_IP
TTL: 300 (or default)
```

### Option 3: Cloudflare Tunnel (Free HTTPS)

**Setup:** `./scripts/setup-friendly-url.sh` → Choose option 3

**URL:** `https://telemer-bot.trycloudflare.com`

**Features:**
- ✅ Free HTTPS subdomain
- ✅ No port forwarding required
- ✅ Works behind NAT/firewall
- ✅ Permanent URL

**Setup Commands:**
```bash
# Install cloudflared
brew install cloudflared  # macOS
# or download from GitHub for Linux

# Run the setup script
./scripts/setup-friendly-url.sh

# Choose option 3
# Get your free subdomain
```

### Option 4: Ngrok Tunnel (Temporary)

**Setup:** `./scripts/setup-friendly-url.sh` → Choose option 4

**URL:** `https://random-string.ngrok.io`

**Features:**
- ✅ Instant setup
- ✅ HTTPS included
- ✅ No configuration required
- ✅ Good for testing

**Setup Commands:**
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Run the setup script
./scripts/setup-friendly-url.sh

# Choose option 4
# Get temporary URL
```

## URL Comparison

| Method | URL Example | SSL | Cost | Permanence | Setup Difficulty |
|---------|--------------|------|-------|-------------|------------------|
| IP Address | `http://167.103.73.80:3001` | ❌ | Free | Permanent | Easy |
| Local Domain | `http://telemer.local` | ❌ | Free | Permanent | Easy |
| Custom Domain | `http://telemer.health` | ✅ | Paid | Permanent | Medium |
| Cloudflare | `https://telemer-bot.trycloudflare.com` | ✅ | Free | Permanent | Medium |
| Ngrok | `https://abc123.ngrok.io` | ✅ | Free | Temporary | Easy |

## Recommended Setup for Different Use Cases

### Development/Testing
**Recommended:** Local Domain (`telemer.local`)
```bash
./scripts/setup-friendly-url.sh
# Choose option 1
```

### Production Deployment
**Recommended:** Custom Domain with SSL
```bash
./scripts/setup-friendly-url.sh
# Choose option 2
# Then setup SSL with Let's Encrypt
```

### Quick Demo/Sharing
**Recommended:** Cloudflare Tunnel
```bash
./scripts/setup-friendly-url.sh
# Choose option 3
```

### Temporary Testing
**Recommended:** Ngrok
```bash
./scripts/setup-friendly-url.sh
# Choose option 4
```

## Configuration Files

### Nginx Configuration (`nginx/public.conf`)
```nginx
server {
    listen 80;
    server_name telemer.local telemer.health telemer.ai;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Access-Control-Allow-Origin "*" always;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Static asset caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker Compose (`docker-compose.public.yml`)
```yaml
version: '3.8'

services:
  webrtc-server:
    image: nginx:alpine
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    volumes:
      - ./nginx/public.conf:/etc/nginx/conf.d/default.conf
      - ./webrtc-client:/usr/share/nginx/html
      - ./ssl:/etc/nginx/ssl
    environment:
      - NGINX_HOST=0.0.0.0
      - NGINX_PORT=80
    restart: unless-stopped
```

## SSL/HTTPS Setup

### Let's Encrypt (Free SSL)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d telemer.health

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Cloudflare SSL (Free)
1. Sign up for Cloudflare account
2. Add your domain to Cloudflare
3. Change nameservers to Cloudflare
4. Enable SSL/TLS in Cloudflare dashboard
5. Choose "Full" or "Flexible" mode

## Troubleshooting

### Local Domain Issues
```bash
# Check hosts file
cat /etc/hosts | grep telemer.local

# Flush DNS cache (macOS)
sudo dscacheutil -flushcache

# Flush DNS cache (Linux)
sudo systemctl restart systemd-resolved

# Test resolution
ping telemer.local
```

### Custom Domain Issues
```bash
# Check DNS propagation
dig telemer.health

# Check nginx configuration
docker exec telemer-bot-free-stack-webrtc-server-1 nginx -t

# Check nginx logs
docker logs telemer-bot-free-stack-webrtc-server-1
```

### Tunnel Issues
```bash
# Check cloudflared status
cloudflared tunnel list

# Check ngrok status
curl http://localhost:4040/api/tunnels

# Restart tunnel
pkill cloudflared
./scripts/setup-friendly-url.sh
```

## Security Considerations

### Production Deployment
1. **Use HTTPS:** Always use SSL in production
2. **Security Headers:** Already configured in nginx
3. **Firewall:** Only open necessary ports
4. **Updates:** Keep Docker images updated
5. **Monitoring:** Set up health checks

### Firewall Rules
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow SSH for management
sudo ufw allow 22

# Enable firewall
sudo ufw enable
```

## Performance Optimization

### Nginx Optimization
```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;

# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Enable HTTP/2 (with SSL)
listen 443 ssl http2;
```

### Browser Caching
```nginx
# Cache static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Testing Your Setup

### Health Check
```bash
# Test local
curl http://telemer.local/health

# Test production
curl https://telemer.health/health
```

### Functionality Test
Open your browser and test these URLs:

1. **Main Interface:** `http://telemer.local`
2. **Health Check:** `http://telemer.local/health`
3. **Medical Test:** "My mother has diabetes"
4. **Call Ending:** "thank you"
5. **Family Tracking:** "My father has chest pain"

## Best Practices

### Domain Names
- **Short and memorable:** `telemer.local`, `telemer.health`
- **Brand relevant:** `telemer.ai`, `telemer-care.com`
- **Easy to spell:** Avoid complex words
- **Professional:** Use .health, .care, .ai, .medical TLDs

### URL Structure
- **Consistent:** Use same URL across all materials
- **HTTPS preferred:** Always use HTTPS when available
- **Redirects:** Set up www to non-www redirects
- **Backup:** Have alternative URLs ready

## Conclusion

User-friendly URLs make your TeleMER Bot:
- ✅ More professional
- ✅ Easier to remember
- ✅ Better for sharing
- ✅ Suitable for production

Choose the setup method that best fits your needs:
- **Local development:** `telemer.local`
- **Production:** Custom domain with SSL
- **Quick sharing:** Cloudflare tunnel
- **Temporary testing:** Ngrok

All options provide the same great TeleMER Bot experience with family member tracking and intelligent call ending!
