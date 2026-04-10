#!/bin/bash

# TeleMER Bot - Vercel Deployment Script
# This script sets up Vercel deployment for public URL access

echo "🚀 TeleMER Bot - Vercel Deployment"
echo "==================================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    
    # Check if npm is available
    if command -v npm &> /dev/null; then
        npm install -g vercel
    elif command -v yarn &> /dev/null; then
        yarn global add vercel
    elif command -v pnpm &> /dev/null; then
        pnpm add -g vercel
    else
        echo "❌ Please install Node.js and npm first"
        echo "Visit: https://nodejs.org/"
        exit 1
    fi
fi

echo "✅ Vercel CLI is installed"
echo ""

# Check if local services are running
echo "🔍 Checking local services..."
ORCHESTRATOR_STATUS=$(curl -s http://localhost:8000/health 2>/dev/null || echo "DOWN")
WEBRTC_STATUS=$(curl -s http://localhost:3001 2>/dev/null || echo "DOWN")

if [ "$ORCHESTRATOR_STATUS" = "DOWN" ]; then
    echo "⚠️  Orchestrator service is not running!"
    echo "   Please start it with: docker-compose up -d"
    echo "   Vercel deployment will work but API calls will fail"
    echo ""
fi

if [ "$WEBRTC_STATUS" = "DOWN" ]; then
    echo "⚠️  WebRTC service is not running!"
    echo "   Please start it with: docker-compose -f docker-compose.webrtc-simple.yml up -d"
    echo ""
fi

echo "📋 Deployment Options:"
echo "===================="
echo "1. Production deployment (vercel.com)"
echo "2. Preview deployment (vercel.app)"
echo "3. Local development server"
echo ""

read -p "Choose deployment type (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🌐 Production Deployment"
        echo "========================"
        
        # Deploy to production
        vercel --prod
        
        echo ""
        echo "✅ Production deployment complete!"
        echo "==============================="
        echo "📱 Your TeleMER Bot is live at:"
        echo "   https://telemer-bot.vercel.app"
        echo ""
        echo "🔧 API Configuration:"
        echo "   Frontend: https://telemer-bot.vercel.app"
        echo "   Backend: http://localhost:8000 (via proxy)"
        echo ""
        echo "📋 Next Steps:"
        echo "1. Ensure local services are running"
        echo "2. Test medical features: \"My mother has diabetes\""
        echo "3. Test call ending: \"thank you\""
        echo "4. Share the public URL with others"
        ;;
        
    2)
        echo ""
        echo "👀 Preview Deployment"
        echo "===================="
        
        # Deploy to preview
        vercel
        
        echo ""
        echo "✅ Preview deployment complete!"
        echo "============================"
        echo "📱 Your TeleMER Bot preview is at:"
        echo "   https://telemer-bot-<random-id>.vercel.app"
        echo ""
        echo "🔧 Features:"
        echo "   • Temporary URL for testing"
        echo "   • Same functionality as production"
        echo "   • Easy to share for feedback"
        ;;
        
    3)
        echo ""
        echo "🏠 Local Development Server"
        echo "=========================="
        
        # Start local development
        vercel dev
        
        echo ""
        echo "✅ Local development server started!"
        echo "================================="
        echo "📱 Local URL: http://localhost:3000"
        echo "🔧 Features:"
        echo "   • Hot reload on changes"
        echo "   • Local API proxy"
        echo "   • Development tools"
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1-3."
        exit 1
        ;;
esac

echo ""
echo "🎉 Vercel Deployment Summary"
echo "==========================="
echo ""
echo "🌐 Public URL: https://telemer-bot.vercel.app"
echo "🔧 API Proxy: /api/* routes to localhost:8000"
echo "📱 Frontend: Served from Vercel CDN"
echo "🏥 Features: Medical coding, family tracking, call ending"
echo ""

echo "📚 Documentation:"
echo "• Vercel Guide: docs/vercel-deployment.md"
echo "• Medical Coding: docs/medical-coding-guide.md"
echo "• Family Tracking: docs/family-member-tracking.md"
echo "• Troubleshooting: docs/troubleshooting-public-access.md"
echo ""

echo "🧪 Testing Your Deployment:"
echo "==========================="
echo "1. Open: https://telemer-bot.vercel.app"
echo "2. Test: \"My mother has diabetes\""
echo "3. Test: \"thank you\" (call ending)"
echo "4. Test: \"My father has chest pain\""
echo ""

echo "🔧 Management Commands:"
echo "======================"
echo "• View logs: vercel logs"
echo "• Redeploy: vercel --prod"
echo "• Remove deployment: vercel remove telemer-bot"
echo "• List deployments: vercel ls"
echo ""

echo "🌟 Your TeleMER Bot is now publicly accessible!"
