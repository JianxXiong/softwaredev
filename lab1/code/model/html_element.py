
#基础HTML元素类，支持标签、子元素、文本内容的操作
#Model层
class HTMLElement:

    def __init__(self, tag, content="", parent=None, element_id=None) -> None:
        self.tag = tag
        self.content = content
        self.children = []
        self.parent = parent
        self.id = element_id if element_id is not None else self.tag

    def add_child(self, child_element) -> None:
        self.children.append(child_element)
        child_element.set_parent(self)

    def set_content(self, content) -> None:
        self.content = content

    def set_id(self, new_id) -> None:
        self.id = new_id

    def set_parent(self, new_parent) -> None:
        self.parent = new_parent
    
    #测试用
    def collect_ids(self, ids):
        if self.id:
            ids.append(self.id)
        for child in self.children:
            child.collect_ids(ids)

    #测试用
    def find_element_by_id(self, target_id):
        if self.element_id == target_id:
            return self
        for child in self.children:
            result = child.find_element_by_id(target_id)
            if result:
                return result
        return None

    def __str__(self) -> str:
        tag_open = f"<{self.tag}{' id="'+self.id+'"' if self.id else ''}>"
        tag_close = f"</{self.tag}>"
        child_content = '\n'.join(str(child) for child in self.children)
        return f"{tag_open}{self.content}{child_content}{tag_close}"

