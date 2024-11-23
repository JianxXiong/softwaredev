import os

class FileManager:
    @staticmethod
    def display_directory(style="tree", open_files=set()):
        # 获取当前目录的所有文件和子文件夹
        current_directory = os.getcwd()
        items = os.listdir(current_directory)

        if style == "tree":
            FileManager._display_tree(current_directory, items, open_files)
        elif style == "indent":
            FileManager._display_indent(current_directory, items, open_files)
        else:
            print("Unknown directory display style.")

    @staticmethod
    def _display_tree(current_directory, items, open_files, prefix=""):
        for i, item in enumerate(items):
            path = os.path.join(current_directory, item)
            connector = "└── " if i == len(items) - 1 else "├── "
            is_open = " *" if item in open_files else ""
            print(f"{prefix}{connector}{item}{is_open}")
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                FileManager._display_tree(path, os.listdir(path), open_files, new_prefix)

    @staticmethod
    def _display_indent(current_directory, items, open_files, level=0):
        indent = "    " * level
        for item in items:
            path = os.path.join(current_directory, item)
            is_open = " *" if item in open_files else ""
            print(f"{indent}{item}{is_open}")
            if os.path.isdir(path):
                FileManager._display_indent(path, os.listdir(path), open_files, level + 1)

    @staticmethod
    def save_file(filepath, content):
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"File saved: {filepath}")
        except Exception as e:
            print(f"Error saving file {filepath}: {e}")

    @staticmethod
    def load_file(filepath):
        if not os.path.exists(filepath):
            print(f"File does not exist: {filepath}")
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            print(f"File loaded: {filepath}")
            return content
        except Exception as e:
            print(f"Error loading file {filepath}: {e}")
            return None
