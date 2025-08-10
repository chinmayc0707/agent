import unittest
from unittest.mock import patch
import os
import shutil
import sys
from io import StringIO

# Add project root to path to allow importing src modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import the main function from the refactored main.py
from main import main

class TestLlmIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test directory."""
        self.original_cwd = os.getcwd()
        self.test_dir = os.path.join(self.original_cwd, "test_llm_integration_dir")

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        os.makedirs(self.test_dir)
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up the temporary test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def _run_main_with_prompt(self, prompt):
        """Helper function to run main.py with a given prompt and capture stdout."""
        # Mock sys.argv
        with patch.object(sys, 'argv', ['main.py', prompt]):
            # Capture stdout
            captured_output = StringIO()
            with patch.object(sys, 'stdout', captured_output):
                main()
            return captured_output.getvalue()

    def test_create_file_integration(self):
        """Test the full flow for creating a file."""
        prompt = "create a file called mock.txt"
        output = self._run_main_with_prompt(prompt)

        # Check that the file was created
        self.assertTrue(os.path.exists("mock.txt"))

        # Check the output messages
        self.assertIn("Using MOCK LLM...", output)
        self.assertIn("Executing command: create-file with args: ['mock.txt']", output)
        self.assertIn("File created at mock.txt", output)

    def test_create_file_with_content_integration(self):
        """Test the full flow for creating a file with content."""
        prompt = "create a file called hello.txt with content 'hello world'"
        output = self._run_main_with_prompt(prompt)

        self.assertTrue(os.path.exists("hello.txt"))
        with open("hello.txt", 'r') as f:
            self.assertEqual(f.read(), "hello world")

        self.assertIn("File created at hello.txt", output)

    def test_create_directory_integration(self):
        """Test the full flow for creating a directory."""
        prompt = "create a directory named my_mock_dir"
        output = self._run_main_with_prompt(prompt)

        self.assertTrue(os.path.isdir("my_mock_dir"))
        self.assertIn("Directory created at my_mock_dir", output)

    def test_move_file_integration(self):
        """Test the full flow for moving a file."""
        # Create the file and directory that the mock prompt expects
        with open("mock.txt", 'w') as f:
            f.write("content")
        os.makedirs("my_mock_dir")

        prompt = "move the file mock.txt to my_mock_dir"
        output = self._run_main_with_prompt(prompt)

        self.assertFalse(os.path.exists("mock.txt"))
        self.assertTrue(os.path.exists(os.path.join("my_mock_dir", "mock.txt")))
        self.assertIn("Moved mock.txt to my_mock_dir", output)

    def test_list_files_integration(self):
        """Test the full flow for listing files."""
        # Create some files and directories to list
        os.makedirs("dir1")
        with open("file1.txt", "w") as f: f.write("")

        prompt = "list all files"
        output = self._run_main_with_prompt(prompt)

        self.assertIn("dir1", output)
        self.assertIn("file1.txt", output)

    def test_invalid_command_from_llm(self):
        """Test that the system handles an invalid command from the LLM."""
        # Patch the mock client to return an invalid command
        with patch('src.llm_client.MockGeminiClient.generate_command') as mock_gen_cmd:
            mock_gen_cmd.return_value = '{"command": "bad-command", "args": []}'

            prompt = "do something bad"
            output = self._run_main_with_prompt(prompt)

            self.assertIn("Error: Invalid command 'bad-command' received from LLM.", output)


if __name__ == '__main__':
    unittest.main()
