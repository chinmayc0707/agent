import argparse
from src.file_system_manager import FileSystemManager

def main():
    parser = argparse.ArgumentParser(description="AI File System Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create file command
    parser_create_file = subparsers.add_parser("create-file", help="Create a new file")
    parser_create_file.add_argument("path", help="The path for the new file")
    parser_create_file.add_argument("content", nargs="?", default="", help="The content of the file")

    # Create directory command
    parser_create_dir = subparsers.add_parser("create-dir", help="Create a new directory")
    parser_create_dir.add_argument("path", help="The path for the new directory")

    # Move command
    parser_move = subparsers.add_parser("move", help="Move a file or directory")
    parser_move.add_argument("source", help="The source path")
    parser_move.add_argument("destination", help="The destination path")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a file or directory")
    parser_delete.add_argument("path", help="The path of the file or directory to delete")

    # List items command
    parser_ls = subparsers.add_parser("ls", help="List items in a directory")
    parser_ls.add_argument("path", nargs="?", default=".", help="The directory path to list items from")

    # Read file command
    parser_cat = subparsers.add_parser("cat", help="Read the content of a file")
    parser_cat.add_argument("path", help="The path of the file to read")

    args = parser.parse_args()
    fs_manager = FileSystemManager()

    if args.command == "create-file":
        result = fs_manager.create_file(args.path, args.content)
        print(result)
    elif args.command == "create-dir":
        result = fs_manager.create_directory(args.path)
        print(result)
    elif args.command == "move":
        result = fs_manager.move(args.source, args.destination)
        print(result)
    elif args.command == "delete":
        result = fs_manager.delete(args.path)
        print(result)
    elif args.command == "ls":
        result = fs_manager.list_items(args.path)
        if isinstance(result, list):
            for item in result:
                print(item)
        else:
            print(result)
    elif args.command == "cat":
        result = fs_manager.read_file(args.path)
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
