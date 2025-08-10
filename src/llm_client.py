import os
import google.generativeai as genai
import json
from abc import ABC, abstractmethod

class LlmClient(ABC):
    """Abstract base class for a Large Language Model client."""

    @abstractmethod
    def __init__(self, system_prompt: str):
        """
        Initializes the client with a system prompt.

        Args:
            system_prompt: The system prompt to guide the LLM's behavior.
        """
        pass

    @abstractmethod
    def generate_command(self, prompt: str) -> str:
        """
        Generates a command based on a user prompt.

        Args:
            prompt: The user's natural language prompt.

        Returns:
            A string containing the LLM's response, expected to be a JSON object.
        """
        pass

class GeminiClient(LlmClient):
    """A client for the Google Gemini API."""

    def __init__(self, system_prompt: str):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            system_instruction=system_prompt
        )

    def generate_command(self, prompt: str) -> str:
        """
        Sends the prompt to the Gemini API and returns the response.
        """
        try:
            response = self.model.generate_content(prompt)
            cleaned_response = self._clean_response(response.text)
            return cleaned_response
        except Exception as e:
            return json.dumps({"error": f"Error generating command from Gemini: {e}"})

    def _clean_response(self, text: str) -> str:
        """
        Cleans the LLM response by removing Markdown formatting for JSON.
        """
        if text.strip().startswith("```json"):
            text = text.strip()[7:].strip()
            if text.endswith("```"):
                text = text[:-3].strip()
        return text


class MockGeminiClient(LlmClient):
    """A mock client that simulates the Gemini API for testing."""

    def __init__(self, system_prompt: str):
        # The system_prompt is ignored in the mock client, but required by the interface
        self.system_prompt = system_prompt
        self.responses = {
            "create a file called mock.txt": json.dumps({
                "command": "create-file",
                "args": ["mock.txt"]
            }),
            "create a file called hello.txt with content 'hello world'": json.dumps({
                "command": "create-file",
                "args": ["hello.txt", "hello world"]
            }),
            "create a directory named my_mock_dir": json.dumps({
                "command": "create-dir",
                "args": ["my_mock_dir"]
            }),
            "list all files": json.dumps({
                "command": "ls",
                "args": ["."]
            }),
             "move the file mock.txt to my_mock_dir": json.dumps({
                "command": "move",
                "args": ["mock.txt", "my_mock_dir"]
            }),
             "delete the file mock.txt": json.dumps({
                "command": "delete",
                "args": ["mock.txt"]
            })
        }

    def generate_command(self, prompt: str) -> str:
        """
        Returns a predefined response for a given prompt.
        """
        return self.responses.get(prompt, json.dumps({"error": "Unknown prompt for mock client"}))
