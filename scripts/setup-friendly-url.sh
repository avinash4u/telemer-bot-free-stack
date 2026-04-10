#!/bin/bash

# TeleMER Bot - User-Friendly URL Setup
# This script helps set up a user-friendly domain name for your TeleMER bot

echo "🌐 TeleMER Bot - User-Friendly URL Setup"
echo "========================================="
echo ""

# Check if running as root for system-wide changes
if [ "$EUID" -eq 0 ]; then
    echo "🔧 Running with system-wide permissions"
    SYSTEM_WIDE=true
else
    echo "👤 Running as user (local setup)"
    SYSTEM_WIDE=false
fi

echo ""
echo "🎯 Choose your setup option:"
echo "==========================="
echo "1. Local domain setup (telemer.local)"
echo "2. Custom domain setup"
echo "3. Cloudflare tunnel (free subdomain)"
echo "4. Ngrok tunnel (temporary URL)"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🏠 Setting up local domain: telemer.local"
        echo "=========================================="
        
        # Stop existing container
        docker-compose -f docker-compose.webrtc-simple.yml down 2>/dev/null
        docker-compose -f docker-compose.public.yml down 2>/dev/null
        
        # Start with user-friendly configuration
        docker-compose -f docker-compose.public.yml up -d
        
        echo ""
        echo "📝 Adding to local hosts file..."
        
        if [ "$SYSTEM_WIDE" = true ]; then
            # System-wide hosts file
            if ! grep -q "telemer.local" /etc/hosts; then
                echo "127.0.0.1 telemer.local" >> /etc/hosts
                echo "✅ Added telemer.local to /etc/hosts"
            else
                echo "✅ telemer.local already exists in /etc/hosts"
            fi
            HOSTS_FILE="/etc/hosts"
        else
            # User hosts file
            USER_HOSTS="$HOME/.hosts"
            if [ ! -f "$USER_HOSTS" ]; then
                touch "$USER_HOSTS"
            fi
            if ! grep -q "telemer.local" "$USER_HOSTS"; then
                echo "127.0.0.1 telemer.local" >> "$USER_HOSTS"
                echo "✅ Added telemer.local to $USER_HOSTS"
                echo "ℹ️  Add this to your /etc/hosts or use: sudo cp $USER_HOSTS /etc/hosts"
            else
                echo "✅ telemer.local already exists in $USER_HOSTS"
            fi
            HOSTS_FILE="$USER_HOSTS"
        fi
        
        echo ""
        echo "🎉 Local domain setup complete!"
        echo "==============================="
        echo "📱 Access URLs:"
        echo "   Local: http://telemer.local"
        echo "   IP:    http://localhost"
        echo ""
        echo "📋 Next steps:"
        echo "1. Open your browser and go to: http://telemer.local"
        echo "2. Test with: \"My mother has diabetes\""
        echo "3. Try call ending: \"thank you\""
        echo ""
        echo "🔧 If telemer.local doesn't work:"
        echo "   • Check your hosts file: $HOSTS_FILE"
        echo "   • Restart your browser"
        echo "   • Clear DNS cache: sudo dscacheutil -flushcache"
        ;;
        
    2)
        echo ""
        echo "🌍 Custom domain setup"
        echo "====================="
        read -p "Enter your domain name (e.g., telemer.yourdomain.com): " domain
        
        if [ -z "$domain" ]; then
            echo "❌ Domain name is required"
            exit 1
        fi
        
        echo ""
        echo "📝 Updating nginx configuration for $domain..."
        
        # Create custom domain config
        cat > nginx/custom.conf << EOF
server {
    listen 80;
    server_name $domain www.$domain;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range" always;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin "*";
    }
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript;
}
EOF
        
        # Update docker-compose to use custom config
        cat > docker-compose.custom.yml << EOF
version: '3.8'

services:
  webrtc-server:
    image: nginx:alpine
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    volumes:
      - ./nginx/custom.conf:/etc/nginx/conf.d/default.conf
      - ./webrtc-client:/usr/share/nginx/html
      - ./ssl:/etc/nginx/ssl
    environment:
      - NGINX_HOST=0.0.0.0
      - NGINX_PORT=80
    restart: unless-stopped
EOF
        
        # Stop existing and start with custom config
        docker-compose -f docker-compose.webrtc-simple.yml down 2>/dev/null
        docker-compose -f docker-compose.public.yml down 2>/dev/null
        docker-compose -f docker-compose.custom.yml up -d
        
        echo ""
        echo "✅ Custom domain configuration created!"
        echo "==================================="
        echo "📱 Access URL: http://$domain"
        echo ""
        echo "📋 DNS setup required:"
        echo "1. Go to your domain registrar"
        echo "2. Create A record: $domain → $(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_PUBLIC_IP')"
        echo "3. Wait for DNS propagation (5-30 minutes)"
        echo ""
        echo "🔧 SSL setup (optional):"
        echo "• Use Let's Encrypt: certbot --nginx -d $domain"
        echo "• Or Cloudflare SSL certificate"
        ;;
        
    3)
        echo ""
        echo "🌐 Cloudflare Tunnel Setup"
        echo "========================="
        echo "This creates a free subdomain like telemer.trycloudflare.com"
        echo ""
        
        # Check if cloudflared is installed
        if ! command -v cloudflared &> /dev/null; then
            echo "📦 Installing cloudflared..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install cloudflared
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
                sudo dpkg -i cloudflared-linux-amd64.deb
            else
                echo "❌ Please install cloudflared manually from: https://github.com/cloudflare/cloudflared/releases"
                exit 1
            fi
        fi
        
        echo "🔧 Starting Cloudflare tunnel..."
        echo "This will create a permanent subdomain for your TeleMER bot"
        echo ""
        
        # Create tunnel configuration
        cat > cloudflare-tunnel.yml << EOF
tunnel: telemer-bot
credentials-file: ~/.cloudflared/credentials.json

ingress:
  - hostname: telemer-bot
    service: http://localhost:3001
  - service: http_status:404
EOF
        
        echo "🚀 Starting tunnel (this may take a moment)..."
        cloudflared tunnel --url http://localhost:3001 --logfile telemer.log &
        CLOUDFLARE_PID=$!
        
        sleep 5
        
        # Try to get the tunnel URL
        if [ -f telemer.log ]; then
            TUNNEL_URL=$(grep -o "https://[^[:space:]]*\.trycloudflare\.com" telemer.log | head -1)
            if [ ! -z "$TUNNEL_URL" ]; then
                echo ""
                echo "✅ Cloudflare tunnel created!"
                echo "============================="
                echo "📱 Public URL: $TUNNEL_URL"
                echo ""
                echo "📋 Features:"
                echo "• Free HTTPS subdomain"
                echo "• No port forwarding required"
                echo "• Works behind NAT/firewall"
                echo "• Permanent URL"
                echo ""
                echo "🔧 Management:"
                echo "• Stop tunnel: kill $CLOUDFLARE_PID"
                echo "• View logs: tail -f telemer.log"
                echo "• Restart: ./scripts/setup-friendly-url.sh (option 3)"
            else
                echo "⚠️  Tunnel URL not found in logs. Check telemer.log"
            fi
        else
            echo "❌ Tunnel log file not created"
        fi
        ;;
        
    4)
        echo ""
        echo "🚀 Ngrok Tunnel Setup (Temporary)"
        echo "================================="
        
        # Check if ngrok is installed
        if ! command -v ngrok &> /dev/null; then
            echo "📦 Installing ngrok..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install ngrok
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                wget -q https://bin.equinox.io/c/4VmDzA7iaHg/ngrok-stable-linux-amd64.zip
                unzip ngrok-stable-linux-amd64.zip
                sudo mv ngrok /usr/local/bin
            else
                echo "❌ Please install ngrok manually from: https://ngrok.com/download"
                exit 1
            fi
        fi
        
        echo "🚀 Starting ngrok tunnel..."
        ngrok http 3001 --log=stdout &
        NGROK_PID=$!
        
        sleep 3
        
        # Get ngrok URL
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o "https://[^[:space:]]*\.ngrok\.io" | head -1)
        
        if [ ! -z "$NGROK_URL" ]; then
            echo ""
            echo "✅ Ngrok tunnel created!"
            echo "========================="
            echo "📱 Temporary URL: $NGROK_URL"
            echo ""
            echo "📋 Features:"
            echo "• Temporary HTTPS URL"
            echo "• No configuration required"
            echo "• Works immediately"
            echo "• Changes each restart"
            echo ""
            echo "⚠️  Limitations:"
            echo "• Free tier has limited bandwidth"
            echo "• URL changes each time"
            echo "• Not suitable for production"
            echo ""
            echo "🔧 Management:"
            echo "• Stop tunnel: kill $NGROK_PID"
            echo "• View web interface: http://localhost:4040"
        else
            echo "❌ Could not retrieve ngrok URL"
            echo "Check ngrok status: http://localhost:4040"
        fi
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1-4."
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo "=================="
echo ""
echo "📚 Documentation:"
echo "• Medical Coding: docs/medical-coding-guide.md"
echo "• Family Tracking: docs/family-member-tracking.md"
echo "• Deployment: docs/deployment-guide.md"
echo ""
echo "🧪 Test your TeleMER Bot:"
echo "========================="
echo "1. Family member: \"My mother has diabetes\""
echo "2. Call ending: \"thank you\""
echo "3. Medical analysis: \"I have chest pain\""
echo ""
echo "🌟 Your TeleMER Bot is ready with a user-friendly URL!"
