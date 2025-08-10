import argparse
import json
from src.file_system_manager import FileSystemManager
from src.llm_client import GeminiClient, MockGeminiClient
from src.prompts import SYSTEM_PROMPT

# A set of allowed commands for validation
ALLOWED_COMMANDS = {
    "create-file",
    "create-dir",
    "move",
    "delete",
    "ls",
    "cat",
}

# Map CLI commands to FileSystemManager method names
COMMAND_TO_METHOD = {
    "create-file": "create_file",
    "create-dir": "create_directory",
    "move": "move",
    "delete": "delete",
    "ls": "list_items",
    "cat": "read_file",
}

def main():
    parser = argparse.ArgumentParser(description="AI File System Agent with LLM")
    parser.add_argument("prompt", help="The natural language prompt for the agent.")
    parser.add_argument("--use-real-llm", action="store_true", help="Use the real Gemini LLM instead of the mock one.")

    args = parser.parse_args()

    # 1. Initialize components
    fs_manager = FileSystemManager()

    if args.use_real_llm:
        print("Using REAL Gemini LLM...")
        try:
            llm_client = GeminiClient(system_prompt=SYSTEM_PROMPT)
        except ValueError as e:
            print(f"Error: {e}")
            print("Please make sure the GOOGLE_API_KEY environment variable is set.")
            return
    else:
        print("Using MOCK LLM...")
        llm_client = MockGeminiClient(system_prompt=SYSTEM_PROMPT)

    # 2. Generate command from LLM
    llm_response_str = llm_client.generate_command(args.prompt)

    # 3. Parse and validate the command
    try:
        command_data = json.loads(llm_response_str)
        if "error" in command_data:
            print(f"LLM Error: {command_data['error']}")
            return

        command = command_data.get("command")
        command_args = command_data.get("args", [])

        if command not in ALLOWED_COMMANDS:
            print(f"Error: Invalid command '{command}' received from LLM.")
            return

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON response from LLM: {llm_response_str}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while parsing the LLM response: {e}")
        return

    # 4. Execute the command
    print(f"Executing command: {command} with args: {command_args}")
    try:
        # Get the actual method name from the map
        method_name = COMMAND_TO_METHOD.get(command)
        if not method_name:
            print(f"Error: Unknown command '{command}'.")
            return

        method_to_call = getattr(fs_manager, method_name)
        result = method_to_call(*command_args)

        # Print the result nicely
        if isinstance(result, list):
            for item in result:
                print(item)
        else:
            print(result)

    except AttributeError:
        print(f"Error: Internal error - command '{command}' has no corresponding method.")
    except TypeError as e:
        print(f"Error: Incorrect arguments for command '{command}'. The LLM may have provided the wrong number of arguments. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during command execution: {e}")


if __name__ == "__main__":
    main()
