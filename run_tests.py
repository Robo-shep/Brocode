import subprocess
import time
import webbrowser
import os
import sys
import threading

def run_flask_server():
    """Run the Flask server in a separate process"""
    print("Starting Flask server...")
    flask_process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the server to start
    time.sleep(2)
    
    return flask_process

def run_api_tests():
    """Run the API tests"""
    print("\n=== Running API Tests ===")
    result = subprocess.run(
        ["python", "test_api.py"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    return result.returncode == 0

def check_frontend_exists():
    """Check if the frontend directory exists and has required files"""
    if not os.path.exists("frontend"):
        print("Error: frontend directory not found")
        return False
    
    required_files = [
        "package.json",
        "src/App.js",
        "src/index.js",
        "public/index.html"
    ]
    
    for file in required_files:
        if not os.path.exists(os.path.join("frontend", file)):
            print(f"Error: {file} not found in frontend directory")
            return False
    
    return True

def main():
    # Check if frontend exists
    if not check_frontend_exists():
        print("Frontend setup is incomplete. Please check the frontend directory.")
        return
    
    # Start Flask server
    flask_process = run_flask_server()
    
    try:
        # Run API tests
        api_tests_passed = run_api_tests()
        
        if api_tests_passed:
            print("\n✅ API tests passed!")
        else:
            print("\n❌ API tests failed!")
        
        # Instructions for testing the frontend
        print("\n=== Frontend Testing Instructions ===")
        print("To test the frontend, follow these steps:")
        print("1. Open a new terminal window")
        print("2. Navigate to the frontend directory: cd frontend")
        print("3. Install dependencies: npm install")
        print("4. Start the development server: npm start")
        print("5. The React app should open automatically in your browser")
        print("6. Use the API Connection Test component to test the connection to the backend")
        
        # Keep the Flask server running
        print("\nPress Ctrl+C to stop the Flask server and exit...")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nStopping Flask server...")
    finally:
        flask_process.terminate()
        print("Tests completed.")

if __name__ == "__main__":
    main()
