import requests
import json
import unittest
import time

class TestMarketResearchAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    def setUp(self):
        # Ensure the Flask server is running before tests
        print("Make sure the Flask server is running (python app.py) before running these tests")
    
    def test_search_endpoint_reddit(self):
        """Test the search endpoint with Reddit platform"""
        endpoint = f"{self.BASE_URL}/api/search"
        payload = {
            "project": "python",
            "platforms": ["reddit"],
            "num_posts": 3
        }
        
        response = requests.post(endpoint, json=payload)
        
        # Print response for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # Print first 200 chars
        
        # Assert response is successful
        self.assertEqual(response.status_code, 200)
        
        # Parse response
        data = response.json()
        
        # Assert response structure
        self.assertIn('project', data)
        self.assertIn('results', data)
        self.assertIn('platform_stats', data)
        self.assertIn('overall_sentiment', data)
        self.assertIn('top_keywords', data)
        
        # Assert project name is correct
        self.assertEqual(data['project'], 'python')
        
        # Assert results contain Reddit data
        if len(data['results']) > 0:
            self.assertEqual(data['results'][0]['platform'], 'Reddit')
    
    def test_search_endpoint_multiple_platforms(self):
        """Test the search endpoint with multiple platforms"""
        endpoint = f"{self.BASE_URL}/api/search"
        payload = {
            "project": "javascript",
            "platforms": ["reddit", "hackernews", "quora"],
            "num_posts": 2
        }
        
        response = requests.post(endpoint, json=payload)
        
        # Assert response is successful
        self.assertEqual(response.status_code, 200)
        
        # Parse response
        data = response.json()
        
        # Assert response structure
        self.assertIn('project', data)
        self.assertIn('results', data)
        self.assertIn('platform_stats', data)
        
        # Assert project name is correct
        self.assertEqual(data['project'], 'javascript')
        
        # Check if we have platform stats for all requested platforms
        for platform in payload['platforms']:
            if platform in data['platform_stats']:
                self.assertIn('positive_percentage', data['platform_stats'][platform])
                self.assertIn('negative_percentage', data['platform_stats'][platform])
                self.assertIn('neutral_percentage', data['platform_stats'][platform])
    
    def test_search_endpoint_invalid_request(self):
        """Test the search endpoint with invalid request"""
        endpoint = f"{self.BASE_URL}/api/search"
        payload = {
            # Missing required 'project' field
            "platforms": ["reddit"]
        }
        
        response = requests.post(endpoint, json=payload)
        
        # We expect the server to handle this gracefully
        self.assertEqual(response.status_code, 200)
        
        # Parse response
        data = response.json()
        
        # Assert response structure
        self.assertIn('project', data)
        self.assertEqual(data['project'], '')  # Should be empty string

if __name__ == "__main__":
    unittest.main()
