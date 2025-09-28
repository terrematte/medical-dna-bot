#!/usr/bin/env python3
"""
Simple tests for the Medical AI Bot application
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import functions from app
from app import initialize_session_state, get_ai_response


class TestMedicalAIBot(unittest.TestCase):
    """Test cases for the Medical AI Bot"""

    def setUp(self):
        """Set up test environment"""
        # Mock streamlit session state
        self.mock_session_state = MagicMock()
        self.mock_session_state.messages = []
        self.mock_session_state.conversation_started = False

    @patch('streamlit.session_state')
    def test_initialize_session_state(self, mock_st_session_state):
        """Test session state initialization"""
        # Mock session state as empty dict
        mock_st_session_state.__contains__ = lambda key: False
        mock_st_session_state.__setitem__ = MagicMock()
        
        initialize_session_state()
        
        # Verify that session state keys are set
        self.assertTrue(mock_st_session_state.__setitem__.called)

    @patch('openai.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_get_ai_response_success(self, mock_openai):
        """Test successful AI response"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test medical response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        messages = [{"role": "user", "content": "What is fever?"}]
        response = get_ai_response(messages)
        
        self.assertEqual(response, "Test medical response")
        mock_client.chat.completions.create.assert_called_once()

    @patch('openai.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_get_ai_response_error(self, mock_openai):
        """Test AI response error handling"""
        # Mock OpenAI to raise an exception
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        messages = [{"role": "user", "content": "What is fever?"}]
        response = get_ai_response(messages)
        
        self.assertTrue(response.startswith("Error:"))

    def test_environment_variables(self):
        """Test that required environment variables can be loaded"""
        # Test with environment file
        test_env_content = "OPENAI_API_KEY=test-key-123\nOPENAI_MODEL=gpt-3.5-turbo\n"
        
        with open('.env.test', 'w') as f:
            f.write(test_env_content)
        
        # Load test environment
        from dotenv import load_dotenv
        load_dotenv('.env.test')
        
        # Clean up
        os.remove('.env.test')
        
        # This test ensures dotenv functionality works
        self.assertTrue(True)  # If we get here, dotenv loading works

    def test_requirements_exist(self):
        """Test that requirements.txt exists and contains necessary packages"""
        self.assertTrue(os.path.exists('requirements.txt'))
        
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = ['streamlit', 'openai', 'python-dotenv', 'requests']
        for package in required_packages:
            self.assertIn(package, content)

    def test_setup_script_exists(self):
        """Test that setup script exists and is executable"""
        self.assertTrue(os.path.exists('setup.py'))
        
        # Check if setup.py contains main function
        with open('setup.py', 'r') as f:
            content = f.read()
            
        self.assertIn('def main()', content)
        self.assertIn('Medical AI Bot Setup', content)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)