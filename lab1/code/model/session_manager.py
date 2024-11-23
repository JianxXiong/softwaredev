import os
import json
from model.html_editor import HTMLEditor
from model.file_manager import FileManager

class SessionManager:
    def __init__(self):
        self.editors = {}  # 存储所有加载的编辑器，键为文件名，值为 HTMLEditor 实例
        self.active_editor = None  # 当前活动的编辑器
        self.modified_files = set()  # 记录有修改的文件但未保存的
        self.showid = {}  # 记录每个文件是否显示ID的设置
        self.load_session_state()  # 尝试恢复上次会话的状态

    def load_session_state(self):
        # 尝试从保存的 session 文件恢复状态
        if os.path.exists("session_state.json"):
            with open("session_state.json", "r") as session_file:
                state = json.load(session_file)
                for filename in state.get("files", []):
                    self.load_editor(filename)
                    self.showid[filename] = state.get("showid", {}).get(filename, True)
                self.active_editor = state.get("active_editor", None)
                if self.active_editor and self.active_editor in self.editors:
                    print(f"Restored active editor: {self.active_editor}")

    def save_session_state(self):
        # 保存当前 session 的状态
        state = {
            "files": list(self.editors.keys()),
            "active_editor": self.active_editor,
            "showid": self.showid
        }
        with open("session_state.json", "w") as session_file:
            json.dump(state, session_file)

    def load_editor(self, filename):
        if filename in self.editors:
            self.active_editor = filename
            print(f"Switched to editor for {filename}")
        else:
            editor = HTMLEditor()
            if os.path.exists(filename):
                editor.read_html(filename)
            else:
                editor.init()
            self.editors[filename] = editor
            self.active_editor = filename
            print(f"Loaded editor for {filename}")

    def save_editor(self, filename):
        if filename in self.editors:
            self.editors[filename].save(filename)
            self.modified_files.discard(filename)
            print(f"Saved {filename}")
        else:
            print(f"No editor found for {filename}")

    def close_editor(self):
        if self.active_editor is None:
            print("No active editor to close.")
            return
        if self.active_editor in self.modified_files:
            save_prompt = input(f"File '{self.active_editor}' has unsaved changes. Save before closing? (yes/no): ")
            if save_prompt.lower() == "yes":
                self.save_editor(self.active_editor)
        del self.editors[self.active_editor]
        self.modified_files.discard(self.active_editor)
        print(f"Closed editor for {self.active_editor}")
        # 选择新的活动编辑器
        if self.editors:
            self.active_editor = next(iter(self.editors))
            print(f"Switched to editor for {self.active_editor}")
        else:
            self.active_editor = None

    def edit_switch(self, filename):
        if filename in self.editors:
            self.active_editor = filename
            print(f"Switched to editor for {filename}")
        else:
            print(f"No editor found for {filename}")

    def list_editors(self):
        if not self.editors:
            print("No editors are currently loaded.")
            return
        for filename in self.editors:
            prefix = "> " if filename == self.active_editor else "  "
            suffix = " *" if filename in self.modified_files else ""
            print(f"{prefix}{filename}{suffix}")

    def set_showid(self, value):
        if self.active_editor:
            self.showid[self.active_editor] = value
            self.editors[self.active_editor].showid = value  # 更新 HTMLEditor 中的 showid
            print(f"Set showid to {value} for {self.active_editor}")
        else:
            print("No active editor to set showid.")

    def dir_display(self, style="tree"):
        FileManager.display_directory(style, self.editors.keys())   

    def run(self):
        print("\nWelcome to the HTML Command Line Editor!\n")
        print("Available commands:")
        print("  load <filename>         - Load or create a new editor for <filename>")
        print("  save <filename>         - Save the specified file")
        print("  close                   - Close the current editor")
        print("  editor-list             - List all open editors")
        print("  edit <filename>         - Switch to the specified editor")
        print("  showid true/false       - Toggle showid for current editor")
        print("  dir-tree                - Display directory in tree format")
        print("  dir-indent              - Display directory in indent format")
        print("  insert <tag> <id> <target_id> [content] - Insert new element before target")
        print("  append <tag> <id> <parent_id> [content] - Append new element inside parent")
        print("  edit-id <old_id> <new_id> - Edit the id of an element")
        print("  edit-text <element_id> [new_content] - Edit text content of an element")
        print("  delete <element_id>     - Delete an element")
        print("  undo                    - Undo the last operation")
        print("  redo                    - Redo the last undone operation")
        print("  spell-check             - Perform spell check on the document")
        print("  print-tree              - Display the HTML structure as a tree")
        print("  print-indent [indent]   - Display HTML with indentation")
        print("  help                    - Display this help message")
        print("  exit                    - Exit the program\n")

        while True:
            command = input("\nhtml-editor> ").strip()
            if command == "help":
                print("\nAvailable commands:")
                print("  load <filename>         - Load or create a new editor for <filename>")
                print("  save <filename>         - Save the specified file")
                print("  close                   - Close the current editor")
                print("  editor-list             - List all open editors")
                print("  edit <filename>         - Switch to the specified editor")
                print("  showid true/false       - Toggle showid for current editor")
                print("  dir-tree                - Display directory in tree format")
                print("  dir-indent              - Display directory in indent format")
                print("  insert <tag> <id> <target_id> [content] - Insert new element before target")
                print("  append <tag> <id> <parent_id> [content] - Append new element inside parent")
                print("  edit-id <old_id> <new_id> - Edit the id of an element")
                print("  edit-text <element_id> [new_content] - Edit text content of an element")
                print("  delete <element_id>     - Delete an element")
                print("  undo                    - Undo the last operation")
                print("  redo                    - Redo the last undone operation")
                print("  spell-check             - Perform spell check on the document")
                print("  print-tree              - Display the HTML structure as a tree")
                print("  print-indent [indent]   - Display HTML with indentation")
                print("  exit                    - Exit the program\n")
            elif command.startswith("load"):
                _, filename = command.split(maxsplit=1)
                self.load_editor(filename)
            elif command.startswith("save"):
                _, filename = command.split(maxsplit=1)
                self.save_editor(filename)
            elif command == "close":
                self.close_editor()
            elif command == "editor-list":
                self.list_editors()
            elif command.startswith("edit"):
                _, filename = command.split(maxsplit=1)
                self.edit_switch(filename)
            elif command == "showid true":
                self.set_showid(True)
            elif command == "showid false":
                self.set_showid(False)
            elif command == "dir-tree":
                self.dir_display(style="tree")
            elif command == "dir-indent":
                self.dir_display(style="indent")
            elif command == "exit":
                self.save_session_state()
                print("Session saved. Exiting...")
                break
            else:
                if self.active_editor is None:
                    print("No active editor. Please load or edit a file first.")
                    continue
                
                editor = self.editors[self.active_editor]
                if command.startswith("insert"):
                    commands = command.split(" ")
                    if len(commands) < 4:
                        print("Usage: insert <tag> <id> <target_id> [content]")
                        continue
                    tag, id, target_id = commands[1:4]
                    content = "" if len(commands) == 4 else " ".join(commands[4:])
                    editor.insert_before(target_id=target_id, new_element_id=id, new_element_tag=tag, new_element_content=content)
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command.startswith("append"):
                    commands = command.split(" ")
                    if len(commands) < 4:
                        print("Usage: append <tag> <id> <parent_id> [content]")
                        continue
                    tag, id, parent_id = commands[1:4]
                    content = "" if len(commands) == 4 else " ".join(commands[4:])
                    editor.add_into(parent_id=parent_id, new_element_id=id, new_element_tag=tag, new_element_content=content)
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command.startswith("edit-id"):
                    commands = command.split(" ")
                    if len(commands) != 3:
                        print("Usage: edit-id <old_id> <new_id>")
                        continue
                    target_id, new_id = commands[1:]
                    editor.edit_element_id(target_id=target_id, new_id=new_id)
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command.startswith("edit-text"):
                    commands = command.split(" ")
                    if len(commands) < 2:
                        print("Usage: edit-text <element_id> [new_content]")
                        continue
                    target_id = commands[1]
                    new_content = "" if len(commands) == 2 else " ".join(commands[2:])
                    editor.edit_element_content(target_id=target_id, new_content=new_content)
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command.startswith("delete"):
                    commands = command.split(" ")
                    if len(commands) != 2:
                        print("Usage: delete <element_id>")
                        continue
                    target_id = commands[1]
                    editor.delete_element(target_id=target_id)
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command == "undo":
                    editor.undo()
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command == "redo":
                    editor.redo()
                    self.modified_files.add(self.active_editor)  # 标记文件已修改
                elif command == "spell-check":
                    editor.check_spelling()
                elif command == "print-tree":
                    editor.print_tree()
                elif command.startswith("print-indent"):
                    commands = command.split(" ")
                    indent = 2 if len(commands) == 1 else int(commands[1])
                    editor.print_indent(indent=indent)
                else:
                    print("Unknown command. Please try again.")

if __name__ == "__main__":
    session = SessionManager()
    session.run()
