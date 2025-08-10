import os
import shutil

class FileSystemManager:
    """
    A class to manage file system operations.
    """

    def create_file(self, path, content=""):
        """
        Creates a file at the given path with optional content.
        """
        try:
            with open(path, 'w') as f:
                f.write(content)
            return f"File created at {path}"
        except Exception as e:
            return f"Error creating file: {e}"

    def create_directory(self, path):
        """
        Creates a directory at the given path.
        """
        try:
            os.makedirs(path, exist_ok=True)
            return f"Directory created at {path}"
        except Exception as e:
            return f"Error creating directory: {e}"

    def move(self, source, destination):
        """
        Moves a file or directory from source to destination.
        """
        try:
            shutil.move(source, destination)
            return f"Moved {source} to {destination}"
        except Exception as e:
            return f"Error moving {source}: {e}"

    def delete(self, path):
        """
        Deletes a file or directory at the given path.
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"File deleted: {path}"
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return f"Directory deleted: {path}"
            else:
                return f"Error: Path not found: {path}"
        except Exception as e:
            return f"Error deleting {path}: {e}"

    def list_items(self, path="."):
        """
        Lists items in a directory.
        """
        try:
            items = os.listdir(path)
            return items
        except Exception as e:
            return f"Error listing items in {path}: {e}"

    def read_file(self, path):
        """
        Reads the content of a file.
        """
        try:
            with open(path, 'r') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file {path}: {e}"
