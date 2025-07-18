import sys
import unittest
from unittest.mock import patch, Mock

sys.path.append(".")
from docs_and_training import docs_and_training, DocsAndTrainingInput

class TestDocsAndTrainingTool(unittest.TestCase):
    @patch('docs_and_training.requests.post')
    def test_successful_json_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "answer": "AWS CDK is a framework for defining cloud infrastructure in code."
        }
        mock_post.return_value = mock_response
        input_data = DocsAndTrainingInput(prompt="What is AWS CDK?")
        result = docs_and_training(input_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("answer", result)
        print("JSON Response Test Result:", result)

    @patch('docs_and_training.requests.post')
    def test_successful_text_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("Not JSON")
        mock_response.text = "AWS CDK is a framework for defining cloud infrastructure in code."
        mock_post.return_value = mock_response
        input_data = DocsAndTrainingInput(prompt="What is AWS CDK?")
        result = docs_and_training(input_data)
        self.assertEqual(result["status"], "success")
        self.assertIn("answer", result)
        print("Text Response Test Result:", result)

    @patch('docs_and_training.requests.post')
    def test_api_error_response(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        input_data = DocsAndTrainingInput(prompt="Some query that causes server error")
        result = docs_and_training(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)
        print("Error Response Test Result:", result)

    @patch('docs_and_training.requests.post')
    def test_connection_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        input_data = DocsAndTrainingInput(prompt="Test timeout query")
        result = docs_and_training(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("timeout", result["error"].lower())
        print("Timeout Test Result:", result)

    @patch('docs_and_training.requests.post')
    def test_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError()
        input_data = DocsAndTrainingInput(prompt="Test connection error query")
        result = docs_and_training(input_data)
        self.assertEqual(result["status"], "error")
        self.assertIn("connection", result["error"].lower())
        print("Connection Error Test Result:", result)

    def test_input_validation(self):
        input_data = DocsAndTrainingInput(prompt="Valid prompt", api_endpoint="http://example.com/api")
        self.assertEqual(input_data.prompt, "Valid prompt")
        self.assertEqual(input_data.api_endpoint, "http://example.com/api")
        input_data_default = DocsAndTrainingInput(prompt="Test prompt")
        self.assertTrue(input_data_default.api_endpoint.startswith("http://"))
        print("Input Validation Test Passed")

if __name__ == "__main__":
    import requests
    print("Running Docs and Training Tool Tests...")
    unittest.main(verbosity=2)
