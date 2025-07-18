import sys
import unittest
from unittest.mock import patch, Mock

sys.path.append(".")

# Import the function directly since we can't import the tool in the example directory
from data_analyst import analyze_data, DataAnalystInput


class TestDataAnalystTool(unittest.TestCase):
    
    @patch('data_analyst.requests.post')
    def test_successful_json_response(self, mock_post):
        """Test successful API call with JSON response"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "analysis": "Top games analysis",
            "top_games": ["Game 1", "Game 2", "Game 3"],
            "total_sales": "150M units"
        }
        mock_post.return_value = mock_response
        
        # Test input
        input_data = DataAnalystInput(
            prompt="What were the best selling games in the last 10 years?"
        )
        
        result = analyze_data(input_data)
        
        # Assertions
        self.assertEqual(result["status"], "success")
        self.assertIn("analysis", result)
        self.assertIn("source_name", result)
        self.assertEqual(result["source_name"], "Data Analyst Assistant")
        print("JSON Response Test Result:", result)
    
    @patch('data_analyst.requests.post')
    def test_successful_text_response(self, mock_post):
        """Test successful API call with text response"""
        # Mock successful response with text
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("Not JSON")  # Simulate JSON decode error
        mock_response.text = "This is a text response with game analysis data."
        mock_post.return_value = mock_response
        
        input_data = DataAnalystInput(
            prompt="Analyze gaming market trends"
        )
        
        result = analyze_data(input_data)
        
        print("Text Response Debug Result:", result)
        self.assertEqual(result["status"], "success")
        self.assertIn("analysis", result)
        self.assertEqual(result["analysis"], "This is a text response with game analysis data.")
        print("Text Response Test Result:", result)
    
    @patch('data_analyst.requests.post')
    def test_api_error_response(self, mock_post):
        """Test API error response"""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        input_data = DataAnalystInput(
            prompt="Some query that causes server error"
        )
        
        result = analyze_data(input_data)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        self.assertIn("500", result["error"])
        print("Error Response Test Result:", result)
    
    @patch('data_analyst.requests.post')
    def test_connection_timeout(self, mock_post):
        """Test connection timeout"""
        # Mock timeout
        mock_post.side_effect = requests.exceptions.Timeout()
        
        input_data = DataAnalystInput(
            prompt="Test timeout query"
        )
        
        result = analyze_data(input_data)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("timeout", result["error"].lower())
        print("Timeout Test Result:", result)
    
    @patch('data_analyst.requests.post')
    def test_connection_error(self, mock_post):
        """Test connection error"""
        # Mock connection error
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        input_data = DataAnalystInput(
            prompt="Test connection error query"
        )
        
        result = analyze_data(input_data)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("connection", result["error"].lower())
        print("Connection Error Test Result:", result)
    
    def test_input_validation(self):
        """Test input validation"""
        # Test with valid input
        input_data = DataAnalystInput(
            prompt="Valid prompt",
            api_endpoint="http://example.com/api"
        )
        
        self.assertEqual(input_data.prompt, "Valid prompt")
        self.assertEqual(input_data.api_endpoint, "http://example.com/api")
        
        # Test with default endpoint
        input_data_default = DataAnalystInput(prompt="Test prompt")
        self.assertTrue(input_data_default.api_endpoint.startswith("http://"))
        print("Input Validation Test Passed")


if __name__ == "__main__":
    # Add requests import for the test
    import requests
    
    print("Running Data Analyst Tool Tests...")
    unittest.main(verbosity=2)
