from model.html_element import HTMLElement
from model.html_document import HTMLDocument
import os
from copy import deepcopy
from bs4 import BeautifulSoup


#命令行HTML编辑器，允许用户操作HTML文档
#Controller层
class HTMLEditor:
    
    def __init__(self) -> None:
        self.document = None
        self.initialized = False
        self.history = []
        self.redo_stack = []
        self.showid = True

    #初始化空html
    def init(self) -> None:
        print("Initializing a new HTML document...")
        self.document = HTMLDocument(title="My Webapp")
        self.initialized = True
        print("New document created.")

    #从html中加载
    def read_html(self, file_path) -> None:
        print(f"Reading HTML file from {file_path}...")
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return
        with open(file_path, 'r', encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        
        if soup.html:
            title_tag = soup.title.string if soup.title else "Untitled"
            self.document = HTMLDocument(title=title_tag)
            ids = []
            html_element = self._build_element_tree(soup.html, ids=ids)
            self.document.html = html_element
            self.document.set_ids(ids)
            self.initialized = True
            print("Document initialized from file.")
        else:
            print("Load html failed.")

    #读取html的辅助函数
    def _build_element_tree(self, bs_element, parent=None, ids=[]) -> HTMLElement:
            tag_name = bs_element.name
            element_id = bs_element.get("id", tag_name)
            ids.append(element_id)
            content = bs_element.string if bs_element.string else ""
            element = HTMLElement(tag=tag_name, content=content.strip(), element_id=element_id)
            
            # 如果有父元素，则添加为父元素的子元素
            if parent:
                parent.add_child(element)
            
            # 遍历子元素并递归添加
            for child in bs_element.children:
                if child.name:  # 跳过字符串节点，只处理标签节点
                    self._build_element_tree(child, element, ids=ids)
            
            return element

    #在某元素前插入元素
    def insert_before(self, target_id, new_element_id, new_element_content, new_element_tag) -> None:
        self._save_state()
        self.document.insert_before(target_id=target_id, new_element=HTMLElement(tag=new_element_tag, content=new_element_content, element_id=new_element_id))


    #向某元素内部添加子元素
    def add_into(self, parent_id, new_element_id, new_element_content, new_element_tag) -> None:
        self._save_state()
        self.document.add_into(target_id=parent_id, new_element=HTMLElement(tag=new_element_tag, element_id=new_element_id, content=new_element_content, parent=parent_id))
        print("son element has been added")

   
    #修改元素id
    def edit_element_id(self, target_id, new_id) -> None:
        self._save_state()
        self.document.edit_element_id(target_id=target_id, new_id=new_id)

    #修改元素文本
    def edit_element_content(self, target_id, new_content) -> None:
        self._save_state()
        self.document.edit_element_content(target_id=target_id, new_content=new_content)

    #删除某元素
    def delete_element(self, target_id) -> None:
        self._save_state()
        self.document.delete_element(element_id=target_id)

    #缩进格式
    def print_indent(self, indent) -> None:
        self.document.display_indent_structure(indent=indent)

    #树的格式
    def print_tree(self) -> None:
        self.document.display_tree_structure(showid=self.showid)

    #拼写检查
    def check_spelling(self) -> None:
        self.document.check_spelling()

    #写入html文件
    def save(self, save_path):
        self.document.save(file_path=save_path)

    #多步重做
    def redo(self) -> None:
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        self.history.append(deepcopy(self.document))
        self.document = self.redo_stack.pop()
        print("Redo operation completed.")

    #多步撤销操作
    def undo(self) -> None:
        if not self.history:
            print("Nothing to undo.")
            return
        self.redo_stack.append(deepcopy(self.document))
        self.document = self.history.pop()  
        print("Undo operation completed.")

    def _save_state(self) -> None:
        self.history.append(deepcopy(self.document))
        self.redo_stack.clear()


if __name__=="__main__":
    html_editor = HTMLEditor()
    html_editor.run()
    