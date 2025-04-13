import requests
import json
import webbrowser
import os
import time
import http.server
import socketserver
import threading
from urllib.parse import parse_qs, urlparse

# HTML template for our simple frontend test
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Research Bot - Frontend Test</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #282c34;
            color: white;
            padding: 20px;
            text-align: center;
        }
        h1 {
            margin: 0;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        .checkbox-group {
            display: flex;
            gap: 15px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 4px;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            margin-top: 20px;
            background-color: white;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .error {
            background-color: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .loading {
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>Market Research Bot</h1>
        <p>A lightweight, real-time market intelligence tool for product builders</p>
    </header>
    <div class="container">
        <h2>API Connection Test</h2>
        <div class="form-group">
            <label for="searchTerm">Search Term:</label>
            <input type="text" id="searchTerm" value="python">
        </div>
        <div class="form-group">
            <label>Select Platforms:</label>
            <div class="checkbox-group">
                <label>
                    <input type="checkbox" id="reddit" checked> Reddit
                </label>
                <label>
                    <input type="checkbox" id="hackernews"> Hacker News
                </label>
                <label>
                    <input type="checkbox" id="quora"> Quora
                </label>
            </div>
        </div>
        <button id="searchButton">Test API Connection</button>
        <div id="loading" class="loading" style="display: none;">
            <p>Loading... This may take a moment.</p>
        </div>
        <div id="error" class="error" style="display: none;"></div>
        <div id="results" class="results" style="display: none;"></div>
    </div>

    <script>
        document.getElementById('searchButton').addEventListener('click', function() {
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            
            // Get form values
            const searchTerm = document.getElementById('searchTerm').value;
            const platforms = [];
            if (document.getElementById('reddit').checked) platforms.push('reddit');
            if (document.getElementById('hackernews').checked) platforms.push('hackernews');
            if (document.getElementById('quora').checked) platforms.push('quora');
            
            // Validate
            if (platforms.length === 0) {
                document.getElementById('error').textContent = 'Please select at least one platform';
                document.getElementById('error').style.display = 'block';
                document.getElementById('loading').style.display = 'none';
                return;
            }
            
            // Make API request
            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    project: searchTerm,
                    platforms: platforms,
                    num_posts: 5
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                // Display results
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = `
                    <h3>API Response:</h3>
                    <h4>Project: ${data.project}</h4>
                    
                    <h4>Overall Sentiment:</h4>
                    <ul>
                        <li>Positive: ${data.overall_sentiment.positive_percentage.toFixed(2)}%</li>
                        <li>Neutral: ${data.overall_sentiment.neutral_percentage.toFixed(2)}%</li>
                        <li>Negative: ${data.overall_sentiment.negative_percentage.toFixed(2)}%</li>
                    </ul>
                    
                    <h4>Top Keywords:</h4>
                    <ul>
                        ${data.top_keywords.map(item => `<li>${item.keyword}: ${item.count}</li>`).join('')}
                    </ul>
                    
                    <h4>Results Count: ${data.results.length}</h4>
                `;
                
                if (data.results.length > 0) {
                    resultsDiv.innerHTML += `
                        <div>
                            <h4>Sample Result:</h4>
                            <p><strong>Platform:</strong> ${data.results[0].platform}</p>
                            <p><strong>Title:</strong> ${data.results[0].title}</p>
                            <p><strong>Sentiment:</strong> ${data.results[0].sentiment}</p>
                        </div>
                    `;
                }
                
                resultsDiv.style.display = 'block';
            })
            .catch(error => {
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                // Show error
                document.getElementById('error').textContent = 'Error: ' + error.message;
                document.getElementById('error').style.display = 'block';
            });
        });
    </script>
</body>
</html>
"""

class FrontendTestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/search':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Forward the request to the Flask API
            try:
                response = requests.post('http://localhost:5000/api/search', json=data)
                
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_frontend_server(port=8000):
    handler = FrontendTestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print(f"Frontend test server started at http://localhost:{port}")
    httpd.serve_forever()

def run_flask_server():
    """Run the Flask server in a separate process"""
    print("Starting Flask server...")
    os.system("start cmd /k python app.py")
    # Wait for the server to start
    time.sleep(2)

def main():
    # Start Flask server
    run_flask_server()
    
    # Start frontend server in a separate thread
    frontend_thread = threading.Thread(target=run_frontend_server)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # Open browser
    webbrowser.open('http://localhost:8000')
    
    print("Press Ctrl+C to stop the servers...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
