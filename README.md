# AI File System Agent (with LLM)

This project is an intelligent AI agent that understands natural language and performs common file system operations on your behalf. It is powered by a Large Language Model (LLM) to interpret your commands.

## Features

- **Natural Language Interface:** Simply tell the agent what you want to do in plain English.
- **Core File Operations:** Supports creating, moving, deleting, and exploring files and directories.
- **LLM-Powered:** Uses Google Gemini to translate your prompts into executable commands.
- **Safe & Testable:** Includes a mock LLM for safe, offline testing and a validation layer for commands.

## Setup

This project is written in Python and requires a few dependencies.

1.  **Clone the repository** (if you haven't already).

2.  **Install dependencies** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The agent is controlled via the `main.py` script. You provide your command as a single string prompt.

### Using the Mock LLM (Default)

By default, the agent uses a mock LLM that only understands a few predefined prompts. This is useful for testing the application without an internet connection or an API key.

*Usage:*
```bash
python main.py "<your prompt>"
```

*Examples:*
```bash
# Create an empty file
python main.py "create a file called mock.txt"

# Create a file with content
python main.py "create a file called hello.txt with content 'hello world'"

# Create a directory
python main.py "create a directory named my_mock_dir"
```

### Using the Real Google Gemini LLM

To use the real Gemini LLM, you need to have a Google API key.

1.  **Get an API Key:** Obtain an API key from Google AI Studio.

2.  **Set Environment Variable:** Set your API key as an environment variable named `GOOGLE_API_KEY`.
    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    ```

3.  **Run the Agent:** Use the `--use-real-llm` flag when running the agent.

*Usage:*
```bash
python main.py "<your prompt>" --use-real-llm
```

*Examples:*
```bash
# Use your imagination!
python main.py "make a new text file for me called notes and put 'buy milk' in it" --use-real-llm

python main.py "show me what's in the src folder" --use-real-llm

python main.py "rename the file notes to shopping_list" --use-real-llm
```

## Running Tests

The project includes a suite of unit and integration tests to ensure the core logic is working correctly. To run all the tests, use the following command from the project's root directory:

```bash
python -m unittest discover tests
```
This will run both the original tests for the file system manager and the new integration tests for the LLM functionality.
