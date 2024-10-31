from html_element import HTMLElement

#整个html文档，最外层为html元素，包含head和body
class HTMLDocument:

    def __init__(self, title="My Webapp") -> None:
        self.id = ["html", "body", "title", "head"]
        self.html = HTMLElement("html")
        self.body = HTMLElement("body")
        self.head = HTMLElement("head")
        self.title = HTMLElement("title", content=title)

        self.html.add_child(self.title)
        self.html.add_child(self.head)
        self.html.add_child(self.body)

    def set_title(self, new_title) -> None:
        self.title.set_content(new_title)

    
    def find_element_by_id(self, element, target_id):
            for child in element.children:
                if child.id == target_id:
                    return child
                res = self.find_element_by_id(child, target_id)
                if res is not None:
                    return res
            return None

    #在某元素后插入元素
    def insert_after(self, target_id, new_element) -> None:
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            parent = target_element.parent
            if parent:
                index = parent.children.index(target_element)
                if index < len(parent.children) - 1:
                    parent.children.insert(index + 1, new_element)
                    new_element.set_parent = parent
                else:
                    parent.add_child(new_element)
        else:
            print(f"Element with id '{target_id}' not found.")

    #向某元素内部添加子元素
    def add_into(self, target_id, new_element) -> None:
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            target_element.add_child(new_element)
        else:
            print(f"Element with id '{target_id}' not found.")

    #树的格式
    def _display_tree(self, element, level, is_first, is_last, prefix):
        connector = "└── " if is_last else "├── "
        if is_first:
            connector = ""
        print(f"{prefix}{connector}{element.tag}{'#' + element.id if element.id else ''}")
        new_prefix = prefix + ("    " if is_last else "│   ")
        child_count = len(element.children)
        for i, child in enumerate(element.children):
            self._display_tree(child, level + 1, False, is_last=(i == child_count - 1), prefix=new_prefix)

    #缩进格式
    def _display_indent(self, element, level) -> None:
        indent = "    " * level
        id_part = f' id="{element.id}"' if element.id else ''
        tag_open = f"{indent}<{element.tag}{id_part}> "
        content = element.content
        if element.tag in ['title', 'h1', 'p', 'li']:
            print(f"{tag_open}{content}</{element.tag}>")
        else:
            print(f"{tag_open}{content}")
            for child in element.children:
                self._display_indent(child, level + 1)
            print(f"{indent}</{element.tag}>")

    def display_tree_structure(self) -> None:
        self._display_tree(self.html, level=0, is_first=True, is_last=True, prefix="")

    
    def display_indent_structure(self) -> None:
        self._display_indent(self.html, 0)

if __name__ == "__main__":
    document = HTMLDocument(title="My Webapp")
    res = document.display_indent_structure()