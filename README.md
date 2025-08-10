# AI File System Agent

This project is a simple command-line based AI agent that can perform common file system operations. It provides a clean interface for creating, moving, deleting, and exploring files and directories.

## Features

- Create files (with or without content)
- Create directories
- Move files and directories
- Delete files and directories
- List the contents of a directory
- Read the contents of a file

## Setup

This project is written in Python and has no external dependencies. You only need a Python 3.x environment to run it.

## Usage

The agent is controlled via the `main.py` script. You can see a list of all available commands by running:

```bash
python main.py --help
```

### Commands

Here are the available commands and how to use them:

**1. `create-file`**

Creates a new file.

*Usage:*
```bash
python main.py create-file <path> [content]
```

*Example:*
```bash
# Create an empty file
python main.py create-file my_new_file.txt

# Create a file with content
python main.py create-file another_file.txt "This is some content."
```

**2. `create-dir`**

Creates a new directory.

*Usage:*
```bash
python main.py create-dir <path>
```

*Example:*
```bash
python main.py create-dir my_new_folder
```

**3. `move`**

Moves a file or directory.

*Usage:*
```bash
python main.py move <source> <destination>
```

*Example:*
```bash
# Move a file into a directory
python main.py move my_new_file.txt my_new_folder/

# Rename a file
python main.py move another_file.txt renamed_file.txt
```

**4. `delete`**

Deletes a file or directory. This is a permanent action.

*Usage:*
```bash
python main.py delete <path>
```

*Example:*
```bash
python main.py delete renamed_file.txt
python main.py delete my_new_folder
```

**5. `ls`**

Lists the contents of a directory. If no path is provided, it lists the contents of the current directory.

*Usage:*
```bash
python main.py ls [path]
```

*Example:*
```bash
python main.py ls
python main.py ls src/
```

**6. `cat`**

Reads and prints the content of a file.

*Usage:*
```bash
python main.py cat <path>
```

*Example:*
```bash
python main.py cat src/file_system_manager.py
```

## Running Tests

The project includes a suite of unit tests to ensure the core logic is working correctly. To run the tests, use the following command from the project's root directory:

```bash
python -m unittest discover tests
```
