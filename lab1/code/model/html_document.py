from html_element import HTMLElement

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

    #在某元素后插入元素
    def insert_after(self, target_id, new_element) -> None:
        if self.whether_exists_element(new_element):
            print(f"element with this id: {new_element.id} already exsists!")
            return
        if self.whether_exists_id(target_id) is False:
            print(f"target element with this id: {target_id} doesn`t exsist!")
            return
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
        else:
            print(f"Element with id '{target_id}' not found.")

    #向某元素内部添加子元素
    def add_into(self, target_id, new_element) -> None:
        if self.whether_exists_element(new_element):
            print(f"element with this id: {new_element.id} already exsists!")
            return
        if self.whether_exists_id(target_id) is False:
            print(f"target element with this id: {target_id} doesn`t exsist!")
            return
        target_element = self.find_element_by_id(self.html, target_id)
        if target_element:
            target_element.add_child(new_element)
            self.ids.append(new_element.id)
        else:
            print(f"Element with id '{target_id}' not found.")

    #修改元素id
    def edit_element_id(self, target_id, new_id) -> None:
        if self.whether_exists_id(new_id):
            print(f"element with this id: {new_id} already exsists!")
            return
        if self.whether_exists_id(target_id) is False:
            print(f"element with this id: {target_id} doesn`t exsists!")
            return
        target_element = self.find_element_by_id(self.html, target_id)
        self.ids[self.ids.index(target_id)] = new_id
        target_element.set_id(new_id)

    #修改元素文本
    def edit_element_content(self, target_id, new_content) -> None:
        if self.whether_exists_id(target_id) is False:
            print(f"element with this id: {target_id} doesn`t exsists!")
            return
        target_element = self.find_element_by_id(self.html, target_id)
        target_element.set_content(new_content)

    #树的格式
    def _display_tree(self, element, level, is_first, is_last, prefix) -> None:
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
    res = document.add_into("body", HTMLElement("h1", "h111111", None, "h11"))
    res = document.add_into("body", HTMLElement("h1", "h111111", None, "h12"))
    res = document.insert_after("h11", HTMLElement("h1", "h111111", None, "h13"))
    res = document.insert_after("h11", HTMLElement("h1", "h111111", None, "h13"))
    res = document.edit_element_id("h11", "h14")
    res = document.edit_element_content("h11", "hahahahha")
    res = document.display_indent_structure()