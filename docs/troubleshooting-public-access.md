# Public Access Troubleshooting Guide

## Issue: Public URL Not Working

**Symptom:** `http://167.103.73.80:3001` returns "504 Gateway Timeout" or "Connection refused"

**Root Cause:** Corporate firewall/proxy blocking external access to your machine

## 🔍 Diagnosis Steps

### 1. Check Local Access
```bash
# Test local access
curl -I http://localhost:3001

# Should return: HTTP/1.1 200 OK
```

### 2. Check Container Status
```bash
# Check if container is running
docker ps | grep webrtc

# Should show container with port mapping
```

### 3. Check Port Binding
```bash
# Check if port is bound correctly
netstat -tulpn | grep :3001

# Should show: 0.0.0.0:3001
```

### 4. Test External Port
```bash
# Test from local machine
telnet localhost 3001

# Should connect successfully
```

## 🛠️ Solutions

### Solution 1: Use Local Domain (Recommended)

**Setup:**
```bash
# Use local domain setup
./scripts/setup-friendly-url.sh
# Choose option 1
```

**Access:** `http://telemer.local`

**Benefits:**
- ✅ Works immediately
- ✅ No firewall issues
- ✅ Professional appearance
- ✅ Perfect for development

### Solution 2: Use Different Port

**Change port mapping:**
```yaml
# Edit docker-compose.public.yml
services:
  webrtc-server:
    ports:
      - "0.0.0.0:8080:80"  # Use 8080 instead of 3001
      - "0.0.0.0:443:443"
```

**Restart service:**
```bash
docker-compose -f docker-compose.public.yml down
docker-compose -f docker-compose.public.yml up -d
```

**Test new port:**
```bash
# Test with different port
curl -I http://167.103.73.80:8080
```

### Solution 3: Cloudflare Tunnel (Best for Corporate Networks)

**Setup:**
```bash
./scripts/setup-friendly-url.sh
# Choose option 3
```

**Result:** `https://telemer-bot.trycloudflare.com`

**Benefits:**
- ✅ Bypasses corporate firewall
- ✅ Free HTTPS
- ✅ No port forwarding needed
- ✅ Works from anywhere

### Solution 4: Ngrok (Quick Testing)

**Setup:**
```bash
./scripts/setup-friendly-url.sh
# Choose option 4
```

**Result:** `https://random-string.ngrok.io`

**Benefits:**
- ✅ Instant setup
- ✅ HTTPS included
- ✅ No configuration required

### Solution 5: VPN Alternative

**If on corporate network:**
1. Connect to personal VPN
2. Test public URL again
3. Use different network if available

## 🔧 Advanced Troubleshooting

### Check Corporate Firewall

**Symptoms:**
- 504 Gateway Timeout
- Connection refused
- Zscaler blocking messages

**Indicators:**
```bash
# Check if response contains Zscaler
curl -s http://167.103.73.80:3001 | grep -i zscaler

# Check for gateway timeout
curl -s http://167.103.73.80:3001 | grep -i "gateway timeout"
```

### Network Diagnostics

**1. Local Network Test:**
```bash
# Test internal connectivity
ping -c 3 127.0.0.1
telnet localhost 3001
```

**2. External Network Test:**
```bash
# Test external connectivity
ping -c 3 8.8.8.8
curl -I https://www.google.com
```

**3. Port Scan:**
```bash
# Check if port is open externally
nmap -p 3001 167.103.73.80

# Or use online tool:
# Visit: https://www.yougetsignal.com/tools/open-ports/
# Enter: 167.103.73.80:3001
```

## 🏢 Corporate Network Solutions

### Option 1: Request Firewall Exception
**Contact IT Department:**
```
Subject: Firewall Exception Request - TeleMER Medical Bot

Dear IT Team,

I need to access a medical consultation application running on my machine.
Please allow inbound connections to:
- IP: 167.103.73.80
- Port: 3001
- Protocol: HTTP/HTTPS
- Purpose: Medical consultation application development

This is for healthcare application testing and development.

Thank you,
[Your Name]
```

### Option 2: Use Development Server
**Alternative deployment:**
```bash
# Deploy to cloud development server
# AWS EC2, Google Cloud, DigitalOcean
# Follow deployment-guide.md
```

### Option 3: Local Testing Only
**Focus on local features:**
```bash
# Use local domain
http://telemer.local

# Test all features locally
# Family member tracking
# Medical coding
# Call ending
```

## 📱 Working Alternatives Right Now

### Option 1: Local Domain (Working)
```
http://telemer.local
```
**Setup:**
```bash
# Add to hosts file if not working
echo "127.0.0.1 telemer.local" >> /etc/hosts

# Or use user hosts file
echo "127.0.0.1 telemer.local" >> ~/.hosts
```

### Option 2: Localhost (Always Working)
```
http://localhost
```
**Setup:**
```bash
# Ensure container is running on port 3001
docker-compose -f docker-compose.webrtc-simple.yml up -d
```

### Option 3: Cloudflare Tunnel (Recommended)
```
https://telemer-bot.trycloudflare.com
```
**Setup:**
```bash
# Install cloudflared
brew install cloudflared

# Start tunnel
cloudflared tunnel --url http://localhost:3001
```

## 🧪 Testing Your Setup

### Test Local Access
```bash
# Test 1: Basic access
curl -I http://localhost:3001

# Test 2: API functionality
curl -X POST http://localhost:3001/health

# Test 3: WebRTC interface
open http://localhost:3001
```

### Test Medical Features
**Open browser and test:**
1. **Family Member Tracking:**
   ```
   "My mother has diabetes"
   "My father has chest pain"
   ```

2. **Call Ending:**
   ```
   "no"
   "thank you"
   "I have no issues"
   ```

3. **Medical Coding:**
   ```
   "I have headache and nausea"
   "I have difficulty breathing"
   ```

## 🔍 Debug Information Collection

### Gather System Info
```bash
# Container status
docker ps | grep webrtc

# Port bindings
docker port telemer-bot-free-stack-webrtc-server-1

# Network info
docker network ls

# System logs
docker logs telemer-bot-free-stack-webrtc-server-1
```

### Network Diagnostics
```bash
# IP configuration
ifconfig | grep inet

# Routing table
netstat -rn

# Firewall status
sudo ufw status

# Process listening
sudo netstat -tulpn | grep :3001
```

## 📋 Quick Fix Checklist

### ✅ Immediate Solutions
- [ ] Use `http://telemer.local` (local domain)
- [ ] Use `http://localhost` (direct access)
- [ ] Try Cloudflare tunnel for HTTPS
- [ ] Use Ngrok for temporary access

### 🔧 Configuration Checks
- [ ] Container running on correct port
- [ ] Port mapping: 0.0.0.0:3001:80
- [ ] No conflicting services on port 3001
- [ ] Firewall allows port 3001

### 🌐 Network Checks
- [ ] Public IP is correct
- [ ] ISP doesn't block port 3001
- [ ] Corporate firewall allows outbound
- [ ] Router port forwarding configured

## 🎯 Recommended Approach

### For Development
1. **Use local domain:** `http://telemer.local`
2. **Test all features locally**
3. **Use Cloudflare tunnel** for external sharing

### For Production
1. **Deploy to cloud server**
2. **Use custom domain**
3. **Setup SSL certificate**
4. **Configure proper DNS**

### For Testing/Demo
1. **Cloudflare tunnel** (free, permanent)
2. **Ngrok** (temporary, quick)
3. **Local domain** (internal testing)

## 📞 Support Resources

### If Issues Persist
1. **Check container logs:**
   ```bash
   docker logs telemer-bot-free-stack-webrtc-server-1
   ```

2. **Verify configuration:**
   ```bash
   docker exec telemer-bot-free-stack-webrtc-server-1 nginx -t
   ```

3. **Test network connectivity:**
   ```bash
   telnet 127.0.0.1 3001
   ```

4. **Restart services:**
   ```bash
   docker-compose -f docker-compose.public.yml restart
   ```

## Conclusion

**The public URL issue is likely caused by:**
- Corporate firewall/proxy blocking
- Network configuration
- Port forwarding not set up

**Working solutions:**
- ✅ `http://telemer.local` (local domain)
- ✅ `http://localhost` (direct access)
- ✅ Cloudflare tunnel (external access)
- ✅ Ngrok (temporary access)

**Choose the solution that best fits your environment and requirements.**

All TeleMER features work perfectly with local access - the issue is external network configuration, not the application itself.
