
Course project.
create a conda environment firstly and then install the require packages:
conda create -n name python=3.12
pip install -r requirements.txt

## todo
### 测试部分没有实现 
代码的测试是软件开发中的重要环节，建议为不同模块引入单元测试和集成测试，以确保各部分的正确性和代码的健壮性。
单元测试：可以使用 Python 的 unittest 或 pytest 框架为每个模块编写单元测试。例如，针对 HTMLEditor 类中的每个方法，编写单独的测试来验证行为是否符合预期。
集成测试：测试整个系统的行为，例如多个编辑器的切换、撤销和重做操作的正确性。

### 将undo和redo换种方式实现，这种方式太占内存。
可以使用**命令模式（Command Pattern）**来实现撤销和重做。每个用户的操作都封装为一个独立的命令对象，这个命令对象有以下两个方法：
execute(): 执行这个命令（比如插入元素、删除元素等）。
undo(): 撤销这个命令。
每次执行用户操作时，将该操作对应的命令对象保存到历史栈中。要撤销时，只需从栈中取出这个命令对象，并调用它的 undo() 方法。这样可以避免每次保存整个文档，只保存修改的“操作记录”。
优点：
更细粒度的控制：每个命令只关注自己相关的那部分修改，不需要处理整个文档。
节省内存：只保存修改操作而不是整个文档。
示例：
class InsertCommand:
    def __init__(self, document, parent_id, new_element):
        self.document = document
        self.parent_id = parent_id
        self.new_element = new_element

    def execute(self):
        self.document.add_into(self.parent_id, self.new_element)

    def undo(self):
        self.document.delete_element(self.new_element.id)

### 重新换结构
1. 分离关注点，增加模块化
目前，SessionManager 中的代码涵盖了多个关注点，包括：
会话管理逻辑
编辑器控制逻辑
命令处理逻辑
可以考虑将这些逻辑拆分成不同的模块，增强项目的模块化和单一责任原则。

a. 创建 CommandHandler 类
将所有命令解析和处理逻辑抽离到一个 CommandHandler 类中，这个类负责解析用户输入的命令并调用 SessionManager 或其他组件的相关方法。这会让 SessionManager 变得更轻量化，并使代码逻辑更加清晰。
command_handler.py
class CommandHandler:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def handle_command(self, command):
        # 这里包含所有的命令解析和处理逻辑
        pass
在 session_manager.py 中引入 CommandHandler，并在 run() 方法中将输入命令传递给 CommandHandler 进行处理。

b. 引入 EditorState 类
考虑创建一个 EditorState 类来管理编辑器的状态（例如是否有修改，当前是否显示 ID 等）。这可以让状态管理变得更集中，避免在多个类中修改状态属性，从而使代码更易于维护。
editor_state.py
class EditorState:
    def __init__(self, filename):
        self.filename = filename
        self.modified = False
        self.showid = True
然后在 SessionManager 中可以维护每个编辑器对应的 EditorState 实例，用来跟踪文件状态。

softwaredev/
    ├── lab1/
        ├── code/
            ├── model/
                ├── __init__.py
                ├── session_manager.py
                ├── command_handler.py   # 新增的命令处理模块
                ├── html_editor.py
                ├── file_manager.py
                ├── editor_state.py      # 新增的编辑器状态管理模块
                ├── utils.py             # 常用工具和辅助函数
            ├── tests/
                ├── test_html_editor.py  # 测试 HTML 编辑器模块
                ├── test_session_manager.py  # 测试 SessionManager
                ├── test_command_handler.py  # 测试 CommandHandler