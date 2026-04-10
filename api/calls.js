// Vercel serverless function for TeleMER API proxy
const fetch = require('node-fetch');

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range',
  'Access-Control-Expose-Headers': 'Content-Length,Content-Range'
};

const ORCHESTRATOR_URL = process.env.ORCHESTRATOR_URL || 'http://localhost:8000';

module.exports = async (req, res) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(200, CORS_HEADERS);
    return res.end();
  }

  try {
    // Get the original URL and query parameters
    const url = new URL(req.url, `http://${req.headers.host}`);
    const path = url.pathname;
    const search = url.search;

    // Only proxy API calls to orchestrator
    if (path.startsWith('/calls/')) {
      const orchestratorUrl = `${ORCHESTRATOR_URL}${path}${search}`;
      
      console.log(`Proxying to: ${orchestratorUrl}`);
      
      const response = await fetch(orchestratorUrl, {
        method: req.method,
        headers: {
          'Content-Type': 'application/json',
          ...req.headers
        },
        body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined
      });

      const data = await response.buffer();
      
      // Forward response with CORS headers
      Object.entries(response.headers).forEach(([key, value]) => {
        if (key.toLowerCase().startsWith('access-control-')) {
          res.setHeader(key, value);
        }
      });

      res.writeHead(response.status, {
        ...CORS_HEADERS,
        'Content-Type': response.headers.get('content-type') || 'application/json'
      });
      
      return res.end(data);
    }

    // For non-API calls, serve the WebRTC client
    if (path === '/' || path === '/index.html') {
      res.setHeader('Content-Type', 'text/html');
      return res.end(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TeleMER Bot - Medical Consultation</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .content {
            padding: 30px;
        }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #4CAF50;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .btn {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 10px 5px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #45a049;
        }
        .btn-secondary {
            background: #2196F3;
        }
        .btn-secondary:hover {
            background: #1976D2;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
        }
        .feature h3 {
            margin-top: 0;
            color: #2196F3;
        }
        .api-info {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 TeleMER Bot</h1>
            <p>AI-Powered Medical Consultation System</p>
        </div>
        <div class="content">
            <div class="info-box">
                <h3>🚀 Public Deployment</h3>
                <p>Your TeleMER Bot is now deployed on Vercel with a public URL!</p>
                <p><strong>Current Status:</strong> API Proxy Active</p>
            </div>

            <div class="features">
                <div class="feature">
                    <h3>🏥 Medical Coding</h3>
                    <p>ICD-10 code generation for 20+ medical conditions with severity assessment</p>
                </div>
                <div class="feature">
                    <h3>👨‍👩‍👧‍👦 Family Tracking</h3>
                    <p>Track medical conditions for mother, father, spouse, child, and siblings</p>
                </div>
                <div class="feature">
                    <h3>📞 Call Management</h3>
                    <p>Intelligent call ending and contextual responses</p>
                </div>
                <div class="feature">
                    <h3>🎤 Speech Recognition</h3>
                    <p>Real-time speech-to-text and text-to-speech capabilities</p>
                </div>
            </div>

            <div class="api-info">
                <h3>🔧 Local Setup Required</h3>
                <p>This Vercel deployment provides the frontend, but requires the local orchestrator service to be running.</p>
                <p><strong>Setup:</strong></p>
                <ol>
                    <li>Start local services: <code>docker-compose up -d</code></li>
                    <li>Ensure orchestrator is accessible: <code>http://localhost:8000</code></li>
                    <li>Test API calls through this proxy</li>
                </ol>
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="http://localhost:3001" class="btn">🏠 Local Development</a>
                <a href="https://github.com/avinash4u/telemer-bot-free-stack" class="btn btn-secondary">📚 Documentation</a>
            </div>
        </div>
    </div>
</body>
</html>
      `);
    }

    // Handle 404
    res.writeHead(404, { 'Content-Type': 'text/html' });
    return res.end(`
<!DOCTYPE html>
<html>
<head><title>404 - Not Found</title></head>
<body>
    <h1>404 - Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <p><a href="/">Go to TeleMER Bot</a></p>
</body>
</html>
    `);

  } catch (error) {
    console.error('Error:', error);
    res.writeHead(500, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ 
      error: 'Internal Server Error',
      message: error.message 
    }));
  }
};
