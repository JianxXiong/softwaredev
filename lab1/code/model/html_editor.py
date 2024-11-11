from .html_element import HTMLElement
from .html_document import HTMLDocument


#命令行HTML编辑器，允许用户操作HTML文档
#Controller层
class HTMLEditor:
    
    def __init__(self) -> None:
        self.document = HTMLDocument()
        self.history = []
        self.redo_stack = []

    def display_document(self) -> None:
        print(self.document)

    def display_tree_structure(self):
        self.document.display_tree_structure()

    def edit_title(self, new_title):
        self.history.append((self.document.title.content, 'title'))
        self.document.set_title(new_title)

    def add_paragraph(self, text, element_id):
        paragraph = HTMLElement("p", content=text, element_id=element_id)
        self.history.append((None, 'add', paragraph))
        self.document.add_to_body(paragraph)

    def undo(self):
        if self.history:
            last_action = self.history.pop()

    def redo(self):
        pass

    #运行命令行界面，处理用户输入的命令
    def run(self) -> None:
        while True:
            command = input("Enter command (view, tree, title, addp, undo, redo, quit): ")
            if command == "view":
                self.display_document()
            elif command == "tree":
                self.display_tree_structure()
            elif command.startswith("title"):
                _, new_title = command.split(" ", 1)
                self.edit_title(new_title)
            elif command.startswith("addp"):
                _, text, element_id = command.split(" ", 2)
                self.add_paragraph(text, element_id)
            elif command == "undo":
                self.undo()
            elif command == "redo":
                self.redo()
            elif command == "quit":
                break
            else:
                print("Unknown command.")
