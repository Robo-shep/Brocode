import requests
import json
import subprocess
import time
import os
import webbrowser
import sys

def start_flask_server():
    """Start the Flask server in a new command window"""
    print("Starting Flask server...")
    try:
        # Start Flask server in a new command window
        subprocess.Popen(["start", "cmd", "/k", "python", "app.py"], 
                         shell=True, 
                         cwd=os.getcwd())
        
        # Wait for the server to start
        print("Waiting for Flask server to start...")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Error starting Flask server: {e}")
        return False

def test_api_endpoint():
    """Test the API endpoint with a simple request"""
    print("\n=== Testing API Endpoint ===")
    
    # Define the endpoint and payload
    endpoint = "http://localhost:5000/api/search"
    payload = {
        "project": "python",
        "platforms": ["reddit"],
        "num_posts": 3
    }
    
    try:
        # Make the request
        print(f"Sending request to {endpoint} with payload: {json.dumps(payload, indent=2)}")
        response = requests.post(endpoint, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("✅ API endpoint test successful!")
            print(f"Status Code: {response.status_code}")
            
            # Parse and display the response
            data = response.json()
            print("\nResponse Summary:")
            print(f"Project: {data.get('project', 'N/A')}")
            
            # Print overall sentiment if available
            if 'overall_sentiment' in data:
                sentiment = data['overall_sentiment']
                print("\nOverall Sentiment:")
                print(f"Positive: {sentiment.get('positive_percentage', 0):.2f}%")
                print(f"Neutral: {sentiment.get('neutral_percentage', 0):.2f}%")
                print(f"Negative: {sentiment.get('negative_percentage', 0):.2f}%")
            
            # Print top keywords if available
            if 'top_keywords' in data and data['top_keywords']:
                print("\nTop Keywords:")
                for keyword in data['top_keywords'][:5]:  # Show top 5 keywords
                    print(f"- {keyword.get('keyword', 'N/A')}: {keyword.get('count', 0)}")
            
            # Print number of results
            if 'results' in data:
                print(f"\nNumber of results: {len(data['results'])}")
                
                # Print sample result if available
                if data['results']:
                    sample = data['results'][0]
                    print("\nSample Result:")
                    print(f"Platform: {sample.get('platform', 'N/A')}")
                    print(f"Title: {sample.get('title', 'N/A')}")
                    print(f"Sentiment: {sample.get('sentiment', 'N/A')}")
            
            return True
        else:
            print(f"❌ API endpoint test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Could not connect to the Flask server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        return False
    
    except Exception as e:
        print(f"❌ Error testing API endpoint: {e}")
        return False

def start_html_frontend():
    """Create and open a simple HTML frontend for testing"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Market Research Bot - Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
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
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .checkboxes {
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
            #results {
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f9f9f9;
                display: none;
            }
            #error {
                margin-top: 20px;
                padding: 15px;
                border: 1px solid #f44336;
                border-radius: 4px;
                background-color: #ffebee;
                color: #c62828;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Market Research Bot</h1>
            <p>Test the API connection by entering a search term and selecting platforms to search.</p>
            
            <div class="form-group">
                <label for="searchTerm">Search Term:</label>
                <input type="text" id="searchTerm" value="python">
            </div>
            
            <div class="form-group">
                <label>Platforms:</label>
                <div class="checkboxes">
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
            
            <button id="searchBtn">Search</button>
            
            <div id="loading" style="display:none; text-align:center; margin-top:20px;">
                Searching... This may take a moment.
            </div>
            
            <div id="error"></div>
            <div id="results"></div>
        </div>
        
        <script>
            document.getElementById('searchBtn').addEventListener('click', function() {
                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';
                document.getElementById('error').style.display = 'none';
                
                // Get values
                const searchTerm = document.getElementById('searchTerm').value;
                const platforms = [];
                if (document.getElementById('reddit').checked) platforms.push('reddit');
                if (document.getElementById('hackernews').checked) platforms.push('hackernews');
                if (document.getElementById('quora').checked) platforms.push('quora');
                
                // Validate
                if (!searchTerm) {
                    document.getElementById('error').textContent = 'Please enter a search term';
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('loading').style.display = 'none';
                    return;
                }
                
                if (platforms.length === 0) {
                    document.getElementById('error').textContent = 'Please select at least one platform';
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('loading').style.display = 'none';
                    return;
                }
                
                // Make API request
                fetch('http://localhost:5000/api/search', {
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
                    
                    let html = `<h3>Results for "${data.project}"</h3>`;
                    
                    // Overall sentiment
                    html += '<h4>Overall Sentiment:</h4>';
                    html += '<ul>';
                    html += `<li>Positive: ${data.overall_sentiment.positive_percentage.toFixed(2)}%</li>`;
                    html += `<li>Neutral: ${data.overall_sentiment.neutral_percentage.toFixed(2)}%</li>`;
                    html += `<li>Negative: ${data.overall_sentiment.negative_percentage.toFixed(2)}%</li>`;
                    html += '</ul>';
                    
                    // Top keywords
                    if (data.top_keywords && data.top_keywords.length > 0) {
                        html += '<h4>Top Keywords:</h4>';
                        html += '<ul>';
                        data.top_keywords.slice(0, 10).forEach(keyword => {
                            html += `<li>${keyword.keyword}: ${keyword.count}</li>`;
                        });
                        html += '</ul>';
                    }
                    
                    // Results count
                    html += `<p>Found ${data.results.length} results</p>`;
                    
                    // Sample result
                    if (data.results.length > 0) {
                        const sample = data.results[0];
                        html += '<h4>Sample Result:</h4>';
                        html += `<p><strong>Platform:</strong> ${sample.platform}</p>`;
                        html += `<p><strong>Title:</strong> ${sample.title}</p>`;
                        html += `<p><strong>Sentiment:</strong> ${sample.sentiment}</p>`;
                    }
                    
                    resultsDiv.innerHTML = html;
                    resultsDiv.style.display = 'block';
                })
                .catch(error => {
                    // Hide loading
                    document.getElementById('loading').style.display = 'none';
                    
                    // Show error
                    document.getElementById('error').textContent = 'Error: ' + error.message;
                    document.getElementById('error').style.display = 'block';
                    
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    """
    
    # Write the HTML to a file
    html_file = "test_frontend.html"
    with open(html_file, "w") as f:
        f.write(html_content)
    
    # Open the HTML file in the default browser
    print(f"\nOpening {html_file} in your default browser...")
    webbrowser.open(f"file://{os.path.abspath(html_file)}")

def main():
    print("=== Market Research Bot Testing ===")
    
    # Start Flask server
    if not start_flask_server():
        print("Failed to start Flask server. Exiting...")
        return
    
    # Test API endpoint
    api_test_success = test_api_endpoint()
    
    if api_test_success:
        # Create and open a simple HTML frontend for testing
        start_html_frontend()
        
        print("\n=== Test Instructions ===")
        print("1. A simple HTML frontend has been opened in your browser")
        print("2. Enter a search term and select platforms to search")
        print("3. Click 'Search' to test the API connection")
        print("4. The Flask server is running in a separate command window")
        print("5. Close the command window to stop the Flask server when done")
    else:
        print("\nAPI test failed. Please check the Flask server and try again.")

if __name__ == "__main__":
    main()
