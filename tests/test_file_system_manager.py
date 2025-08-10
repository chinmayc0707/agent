import unittest
import os
import shutil
import sys

# Add project root to path to allow importing src modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.file_system_manager import FileSystemManager

class TestFileSystemManager(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test directory and a FileSystemManager instance."""
        self.original_cwd = os.getcwd()
        self.test_dir = os.path.join(self.original_cwd, "test_temp_dir")

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        os.makedirs(self.test_dir)
        os.chdir(self.test_dir)

        self.fs_manager = FileSystemManager()

    def tearDown(self):
        """Clean up the temporary test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_create_file(self):
        """Test creating a file."""
        file_path = "test_file.txt"
        content = "Hello, world!"
        self.fs_manager.create_file(file_path, content)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), content)

    def test_create_file_no_content(self):
        """Test creating a file with no content."""
        file_path = "empty_file.txt"
        self.fs_manager.create_file(file_path)
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), "")

    def test_create_directory(self):
        """Test creating a directory."""
        dir_path = "test_subdir"
        self.fs_manager.create_directory(dir_path)
        self.assertTrue(os.path.isdir(dir_path))

    def test_read_file(self):
        """Test reading a file."""
        file_path = "readable_file.txt"
        content = "You can read this."
        with open(file_path, 'w') as f:
            f.write(content)
        read_content = self.fs_manager.read_file(file_path)
        self.assertEqual(read_content, content)

    def test_read_nonexistent_file(self):
        """Test reading a non-existent file."""
        result = self.fs_manager.read_file("nonexistent.txt")
        self.assertTrue("Error reading file" in result)

    def test_list_items(self):
        """Test listing items in a directory."""
        os.makedirs("subdir", exist_ok=True)
        with open("file1.txt", 'w') as f:
            f.write("1")

        items = self.fs_manager.list_items(".")
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn("file1.txt", items)
        self.assertIn("subdir", items)

    def test_move_file(self):
        """Test moving a file."""
        src_file = "move_src.txt"
        dst_dir = "move_dst_dir"
        os.makedirs(dst_dir, exist_ok=True)
        with open(src_file, 'w') as f:
            f.write("move me")

        self.fs_manager.move(src_file, os.path.join(dst_dir, src_file))
        self.assertFalse(os.path.exists(src_file))
        self.assertTrue(os.path.exists(os.path.join(dst_dir, src_file)))

    def test_move_directory(self):
        """Test moving a directory."""
        src_dir = "src_dir_to_move"
        dst_dir = "dst_dir_for_move"
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(dst_dir, exist_ok=True)

        self.fs_manager.move(src_dir, os.path.join(dst_dir, src_dir))
        self.assertFalse(os.path.exists(src_dir))
        self.assertTrue(os.path.isdir(os.path.join(dst_dir, src_dir)))

    def test_delete_file(self):
        """Test deleting a file."""
        file_to_delete = "deletable_file.txt"
        with open(file_to_delete, 'w') as f:
            f.write("delete me")
        self.assertTrue(os.path.exists(file_to_delete))
        self.fs_manager.delete(file_to_delete)
        self.assertFalse(os.path.exists(file_to_delete))

    def test_delete_directory(self):
        """Test deleting a directory."""
        dir_to_delete = "deletable_dir"
        os.makedirs(dir_to_delete)
        self.assertTrue(os.path.isdir(dir_to_delete))
        self.fs_manager.delete(dir_to_delete)
        self.assertFalse(os.path.exists(dir_to_delete))

    def test_delete_nonexistent(self):
        """Test deleting a non-existent path."""
        result = self.fs_manager.delete("nonexistent.path")
        self.assertTrue("Error: Path not found" in result)

if __name__ == '__main__':
    unittest.main()
