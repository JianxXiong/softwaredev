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
        self.document.display_indent_structure()

    def display_tree_structure(self) -> None:
        self.document.display_tree_structure()

    def edit_title(self, new_title) -> None:
        self.history.append((self.document.title.content, 'title'))
        self.document.set_title(new_title)

    #在某元素前插入元素
    def insert_before(self, target_id, new_element_id, new_element_content, new_element_tag) -> None:
        self.document.insert_before(target_id=target_id, new_element=HTMLElement(tag=new_element_tag, content=new_element_content, element_id=new_element_id))
    
    #向某元素内部添加子元素
    def add_into(self, parent_id, new_element_id, new_element_content, new_element_tag) -> None:
        self.document.add_into(target_id=parent_id, new_element=HTMLElement(tag=new_element_tag, id=new_element_id, content=new_element_content, parent=parent_id))
   
    #修改元素id
    def edit_element_id(self, target_id, new_id) -> None:
        self.document.edit_element_id(target_id=target_id, new_id=new_id)

    #修改元素文本
    def edit_element_content(self, target_id, new_content):
        self.document.edit_element_content(target_id=target_id, new_content=new_content)
    def undo(self):
        if self.history:
            last_action = self.history.pop()

    def redo(self):
        pass

    #运行命令行界面，处理用户输入的命令
    def run(self) -> None:
        while True:
            command = input("Enter command (view, tree, title, addp, undo, redo, quit): ")
            if command.startswith("insert"):
                tag, id, target_id, content = command.split(" ")[1:]
                self.insert_before(target_id=target_id, new_element_id=id, new_element_tag=tag, new_element_content=content)
            elif command.startswith("append"):
                tag, id, target_id, content = command.split(" ")[1:]
                self.add_into(parent_id=target_id, new_element_id=id, new_element_tag=tag, new_element_content=content)
            elif command.startswith("edit-id"):
                target_id, new_id = command.split(" ")[1:]
                self.edit_element_id(target_id=target_id, new_id=new_id)
            elif command.startswith("edit-id"):
                target_id, new_content = command.split(" ")[1:]
                self.edit_element_content(target_id=target_id, new_content=new_content)
            elif command == "redo":
                self.redo()
            elif command == "quit":
                break
            else:
                print("Unknown command.")
