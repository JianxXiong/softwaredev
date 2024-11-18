from html_editor import HTMLEditor
import os
import shlex
import platform
import tempfile
import subprocess

class HTMLSession:
    def __init__(self) -> None:
        self.editors = {}
        self.current_directory = os.getcwd()
        self.active_editor = None

    #加载一个编辑器
    def load(self, file_name) -> None:
        full_path = os.path.join(self.current_directory, file_name)
        if file_name not in self.editors:
            editor = HTMLEditor()
            if os.path.exists(full_path):
                editor.read_html(full_path)
            else:
                editor.init()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            editor.save(temp_file.name)
            self.editors[file_name] = {'editor': editor, 'process': None, 'temp_file': temp_file.name, "terminal_window_id": None}
        else:
            print(f"{file_name} is already loaded. Switching to it.")
        #self.set_active_editor(file_name)
        print(f"File '{file_name}' loaded as successfully.")
    
    #保存一个编辑器
    def save(self, file_name) -> None:
        full_path = os.path.join(self.current_directory, file_name)
        if file_name in self.editors:
            self.editors[file_name]['editor'].save(full_path)
        else:
           print(f"No editor open for file '{full_path}'.") 

    #关闭一个编辑器
    def close(self, file_name) -> None:
        if file_name not in self.editors:
            print(f"Error: File '{file_name}' is not currently open.")
            return
        editor_info = self.editors[file_name]
        editor = editor_info['editor']
        if editor.modified:
            response = input(f"File '{file_name}' has unsaved changes. Save before closing? (y/n): ").strip().lower()
            if response == 'y':
                full_path = os.path.join(self.current_directory, file_name)
                editor.save(full_path)

        if editor_info['process'] and editor_info['process'].poll() is None:
            editor_info['process'].terminate()
            editor_info['process'].wait()
            print(f"Closed window for '{file_name}'.")
        
        if editor_info['terminal_window_id']:
            self._close_terminal_window(editor_info['terminal_window_id'])

        os.remove(editor_info['temp_file'])
        print(self.editors[file_name])
        del self.editors[file_name]
        if file_name == self.active_editor:
            self._update_active_editor()

    #显示当前session的编辑器列表
    def editor_list(self) -> None:
        if not self.editors:
            print("No files are currently open.")
            return
        print("Open files in current session:")
        for file_name, editor_info in self.editors.items():
            editor_info['editor'].print_tree()
            modified_mark = "*" if editor_info['editor'].modified else ""
            active_mark = ">" if file_name == self.active_editor else ""
            print(f"{active_mark} {file_name} {modified_mark}")
    
    #切换活动编辑器
    def edit(self, file_name) -> None:
        self.set_active_editor(file_name=file_name)  

    #更新活动编辑器
    def _update_active_editor(self) -> None:
        self.active_editor = next(iter(self.editors), None)

    def get_active_editor(self) -> HTMLEditor:
        return self.editors.get(self.active_editor, None)
    
    #设置活动编辑器，并打开新窗口线程
    def set_active_editor(self, file_name):
        if file_name in self.editors:
            self.active_editor = file_name
            editor_info = self.editors[file_name]
            print(f"Switched to '{file_name}' as active editor.")
            script = f"""
            tell application "Terminal"
                do script "cd {self.current_directory} && conda activate softwaredev && python3 -c \\"from html_editor import HTMLEditor; editor = HTMLEditor(); editor.read_html('{editor_info['temp_file']}'); editor.run()\\""
            end tell
            """
            if platform.system() == "Windows":
                editor_process = subprocess.Popen(
                ["python", "-c", f"from html_editor import HTMLEditor; editor = HTMLEditor(); editor.read_html('{editor_info['temp_file']}'; editor.run()"]
            )
            else:
                editor_process = subprocess.Popen(['osascript', '-e', script])
            editor_info['process'] = editor_process
        else:
            print(f"Error: File '{file_name}' is not currently open.")

    #关闭所有编辑器
    def close_all_editors(self) -> None:
        for file_name in list(self.editors.keys()):
            self.close(file_name=file_name)

    def _close_terminal_window(self, window_id):
        script = f"""
        tell application "Terminal"
            close (every window whose id is {window_id})
        end tell
        """
        subprocess.run(['osascript', '-e', script])

    def run(self) -> None:
        while True:
            command = input("Enter session command (load, save, close, editor-list, edit, exit): ")
            if command.startswith("load"):
                _, filename = command.split(" ")
                self.load(filename)
            elif command.startswith("save"):
                _, filename = command.split(" ", 1)
                self.save(filename)
            elif command.startswith("close"):
                if self.active_editor:
                    self.close(self.active_editor)
                else:
                    print("No active editor to close.")
            elif command.startswith("editor-list"):
                self.editor_list()
            elif command.startswith("edit"):
                _, filename = command.split(" ", 1)
                if filename in self.editors:
                    self.set_active_editor(filename)
                else:
                    print(f"Error: '{filename}' is not open.")
            elif command.startswith("exit"):
                print("Exiting session.")
                self.close_all_editors()
                break
            else:
                print("Unknown command.")

if __name__=="__main__":
    session = HTMLSession()
    session.run()