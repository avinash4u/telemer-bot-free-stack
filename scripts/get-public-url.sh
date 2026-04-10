#!/bin/bash

# TeleMER Bot - Public URL Generator
# This script helps you get the public URL for your deployed WebRTC interface

echo "🚀 TeleMER Bot - Public URL Generator"
echo "======================================"
echo ""

# Check if WebRTC container is running
CONTAINER_STATUS=$(docker ps --filter "name=webrtc-server" --format "{{.Status}}")
if [ -z "$CONTAINER_STATUS" ]; then
    echo "❌ WebRTC server is not running!"
    echo "Please start it with: docker-compose -f docker-compose.webrtc-simple.yml up -d"
    exit 1
fi

echo "✅ WebRTC server is running: $CONTAINER_STATUS"
echo ""

# Try different methods to get public IP
echo "🔍 Detecting public IP address..."

# Method 1: Try curl ifconfig.me
PUBLIC_IP=$(curl -s --connect-timeout 5 --max-time 5 https://ifconfig.me 2>/dev/null)

# Method 2: Try ipinfo.io if above fails
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s --connect-timeout 5 --max-time 5 https://ipinfo.io/ip 2>/dev/null)
fi

# Method 3: Try icanhazip.com if above fails
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s --connect-timeout 5 --max-time 5 https://icanhazip.com 2>/dev/null)
fi

# Method 4: Try internal IP as fallback
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(hostname -I | awk '{print $1}')
    echo "⚠️  Could not detect public IP, using local IP: $PUBLIC_IP"
    echo "    This URL will only work on your local network."
else
    echo "✅ Public IP detected: $PUBLIC_IP"
fi

echo ""

# Generate URLs
LOCAL_URL="http://localhost:3001"
PUBLIC_URL="http://$PUBLIC_IP:3001"

echo "📱 Access URLs:"
echo "================"
echo "Local Access:   $LOCAL_URL"
echo "Public Access:  $PUBLIC_URL"
echo ""

# Test local connectivity
echo "🧪 Testing connectivity..."
if curl -s --connect-timeout 3 "$LOCAL_URL" > /dev/null; then
    echo "✅ Local URL is accessible"
else
    echo "❌ Local URL is not accessible"
fi

# Test public connectivity (only if we have a real public IP)
if [[ "$PUBLIC_IP" != "172."* && "$PUBLIC_IP" != "192."* && "$PUBLIC_IP" != "10."* ]]; then
    if curl -s --connect-timeout 5 "$PUBLIC_URL" > /dev/null; then
        echo "✅ Public URL is accessible"
    else
        echo "⚠️  Public URL may not be accessible from outside your network"
        echo "   Check your firewall settings and ensure port 3001 is open"
    fi
else
    echo "ℹ️  Skipping public URL test (using local IP)"
fi

echo ""
echo "🌐 What you can do with TeleMER Bot:"
echo "=================================="
echo "• 🏥 Medical symptom analysis with ICD-10 coding"
echo "• 👨‍👩‍👧‍👦 Family member health tracking"
echo "• 📞 Intelligent call ending"
echo "• 🎤 Real-time speech recognition"
echo "• 🤖 AI-powered medical responses"
echo ""

echo "📋 Quick Test Commands:"
echo "======================"
echo "Test these phrases in the WebRTC interface:"
echo ""
echo "1. Family member tracking:"
echo "   \"My mother has diabetes\""
echo "   \"My father has chest pain\""
echo ""
echo "2. Call ending:"
echo "   \"no\""
echo "   \"thank you\""
echo "   \"I have no issues\""
echo ""
echo "3. Medical conditions:"
echo "   \"I have headache and nausea\""
echo "   \"I have difficulty breathing\""
echo ""

echo "🔧 Troubleshooting:"
echo "==================="
echo "If the public URL doesn't work:"
echo "1. Check firewall: sudo ufw allow 3001"
echo "2. Check router: Port forward 3001 to your machine"
echo "3. Check cloud provider: Security group allows port 3001"
echo ""

echo "📚 Documentation:"
echo "================"
echo "• Medical Coding Guide: docs/medical-coding-guide.md"
echo "• Family Tracking Guide: docs/family-member-tracking.md"
echo "• Full Deployment Guide: docs/deployment-guide.md"
echo ""

echo "🎉 Your TeleMER Bot is ready!"
echo "================================"
