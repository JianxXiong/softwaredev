from .html_element import HTMLElement
import os
from spellchecker import SpellChecker

#整个html文档，最外层为html元素，包含head和body
#Service层
class HTMLDocument:

    def __init__(self, title="My Webapp") -> None:
        #ids为了方便判断是否存在
        self.ids = ["html", "body", "title", "head"]
        self.html = HTMLElement("html")
        self.body = HTMLElement("body")
        self.head = HTMLElement("head")
        self.title = HTMLElement("title", content=title)

        self.html.add_child(self.title)
        self.html.add_child(self.head)
        self.html.add_child(self.body)

        self.spell_checker = SpellChecker()

    def set_ids(self, new_ids) -> None:
        self.ids = new_ids

    def set_showid(self, showid) -> None:
        self.showid = showid

    #修改title内容
    def set_title(self, new_title) -> None:
        self.title.set_content(new_title)

    #按照元素id判断元素是否存在
    def whether_exists_id(self, id) -> bool:
        if id in self.ids:
            return True
        return False
    
    #判断元素是否存在
    def whether_exists_element(self, element) -> bool:
        return self.whether_exists_id(element.id)
    
    #通过id获取元素
    def find_element_by_id(self, element, target_id):
            if self.whether_exists_id(target_id) is False:
                print(f"target element with this id: {target_id} doesn`t exsist!")
                return None
            for child in element.children:
                if child.id == target_id:
                    return child
                res = self.find_element_by_id(child, target_id)
                if res is not None:
                    return res
            return None
    
    #在某元素前插入元素
    def insert_before(self, target_id, new_element) -> bool:
        if self.whether_exists_element(new_element):
            print(f"element with this id: {new_element.id} already exists!")
            return False
        if self.whether_exists_id(target_id) is False:
            print(f"target element with this id: {target_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            parent = target_element.parent
            if parent:
                index = parent.children.index(target_element)
                parent.children.insert(index, new_element)
                new_element.set_parent(parent)
                self.ids.append(new_element.id)
            return True
        else:
            print(f"Element with id '{target_id}' not found.")
            return False

    #在某元素后插入元素
    def insert_after(self, target_id, new_element) -> bool:
        if self.whether_exists_element(new_element):
            print(f"element with this id: {new_element.id} already exists!")
            return False
        if self.whether_exists_id(target_id) is False:
            print(f"target element with this id: {target_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            parent = target_element.parent
            if parent:
                index = parent.children.index(target_element)
                if index < len(parent.children) - 1:
                    parent.children.insert(index + 1, new_element)
                    new_element.set_parent = parent
                    self.ids.append(new_element.id)
                else:
                    parent.add_child(new_element)
                    self.ids.append(new_element.id)
            return True
        else:
            print(f"Element with id '{target_id}' not found.")
            return False

    #向某元素内部添加子元素
    def add_into(self, target_id, new_element) -> bool:
        if self.whether_exists_element(new_element):
            print(f"element with this id: {new_element.id} already exists!")
            return False
        if self.whether_exists_id(target_id) is False:
            print(f"target element with this id: {target_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            target_element.add_child(new_element)
            self.ids.append(new_element.id)
            return True
        else:
            print(f"Element with id '{target_id}' not found.")
            return False

    #修改元素id
    def edit_element_id(self, target_id, new_id) -> bool:
        if self.whether_exists_id(new_id):
            print(f"element with this id: {new_id} already exists!")
            return False
        if self.whether_exists_id(target_id) is False:
            print(f"element with this id: {target_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, target_id)
        self.ids[self.ids.index(target_id)] = new_id
        target_element.set_id(new_id)
        return True

    #修改元素文本
    def edit_element_content(self, target_id, new_content) -> bool:
        if self.whether_exists_id(target_id) is False:
            print(f"element with this id: {target_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, target_id)
        target_element.set_content(new_content)
        return True

    #删除某元素
    def delete_element(self, element_id) -> bool:
        if not self.whether_exists_id(element_id):
            print(f"element with this id: {element_id} doesn't exist!")
            return False
        target_element = self.find_element_by_id(self.html, element_id)
        parent = target_element.parent
        if parent is not None:
            parent.children.remove(target_element)
        self._remove_element_recursively(target_element)
        return True
    
    #打印树形结构
    def display_tree_structure(self, showid) -> None:
        self._display_tree(self.html, level=0, is_first=True, is_last=True, prefix="", showid=showid)

    #打印缩进结构
    def display_indent_structure(self, indent) -> None:
        self._display_indent(self.html, level=0, indent=indent)

    #拼写检查
    def check_spelling(self) -> None:
        print("Checking spelling in the document...")
        errors = self._check_spelling_recursively(self.html)
        if not errors:
            print("No spelling errors found.")
        else:
            print("Spelling errors found:")
            for word, suggestions in errors.items():
                print(f" - '{word}' may be incorrect. Suggestions: {suggestions}")
    
    #保存html
    def save(self, file_path) -> None:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist.")
            return

        try:
            html_content = self._to_html_string()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(f"HTML document saved to {file_path}")
        except Exception as e:
            print(f"Failed to save HTML document: {e}")

    #树的格式
    def _display_tree(self, element, level, is_first, is_last, prefix, showid) -> None:
        connector = "└── " if is_last else "├── "
        if is_first:
            connector = ""
        if showid:
            print(f"{prefix}{connector}{element.tag}{'#' + element.id if element.id else ''}")
        else:
            print(f"{prefix}{connector}{element.tag}")
        if element.content:
            content_prefix = prefix + ("    " if is_last else "|   ")
            print(f"{content_prefix}└── {element.content}")
        new_prefix = prefix + ("    " if is_last else "│   ")
        child_count = len(element.children)
        for i, child in enumerate(element.children):
            self._display_tree(child, level + 1, False, is_last=(i == child_count - 1), prefix=new_prefix, showid=showid)

    #缩进格式
    def _display_indent(self, element, level, indent=2) -> None:
        indent_str = " " * indent * level
        id_part = f' id="{element.id}"' if element.id else ''
        tag_open = f"{indent_str}<{element.tag}{id_part}> "
        content = element.content
        if element.tag in ['title', 'h1', 'p', 'li']:
            print(f"{tag_open}{content}</{element.tag}>")
        else:
            print(f"{tag_open}{content}")
            for child in element.children:
                self._display_indent(child, level + 1, indent)
            print(f"{indent_str}</{element.tag}>")
    
    #递归删除子元素
    def _remove_element_recursively(self, element) -> None:
        if element.id in self.ids:
            self.ids.remove(element.id)
        for child in element.children:
            self._remove_element_recursively(child)
    
    #递归检查拼写
    def _check_spelling_recursively(self, element) -> dict:
        errors = {}
        if element.content:
            words = element.content.split()
            for word in words:
                if word not in self.spell_checker:  
                    suggestions = self.spell_checker.candidates(word)
                    if suggestions is None:
                        continue
                    errors[word] = list(suggestions)
        
        for child in element.children:
            child_errors = self._check_spelling_recursively(child)
            errors.update(child_errors)
        
        return errors
    
    def _to_html_string(self) -> str:

        return "<!DOCTYPE html>\n" + str(self.html)