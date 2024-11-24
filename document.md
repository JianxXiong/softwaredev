# 基于命令行的多文件 HTML 编辑器

## 1. 项目概述

本项目的是开发一个基于命令行的多文件 HTML 编辑器，支持对 HTML 文档进行基本的增删改查操作，旨在展示对面向对象编程、设计模式及系统架构的理解和应用。该编辑器不仅可以操作单个 HTML 文件，还可以在一个会话（Session）中管理多个文件，实现多个编辑器间的切换、保存、关闭、以及恢复上次的编辑状态。

### 项目目标
- 设计一个面向对象的 HTML 简化版模型，以保存并操作 HTML 内容。
- 提供命令行界面，支持多文件编辑，允许用户对 HTML 文档进行基本操作（如添加、修改、删除元素等）。
- 支持撤销、重做、拼写检查等功能，增强用户体验。

## 2. 项目架构设计

项目采用模块化的设计，每个模块有清晰的职责划分，以便于后续的维护和扩展。

### 系统整体架构

整个项目可以分为多个模块，每个模块承担不同的职责，共同完成多文件 HTML 编辑的功能。这些模块主要包括：管理会话的 `SessionManager`、处理具体 HTML 操作的 `HTMLEditor`、提供文件管理的 `FileManager`，以及代表 HTML 文档结构的 `HTMLDocument` 和 `HTMLElement`。

- **SessionManager** 负责整体会话的管理，它是整个编辑器的核心调度模块。用户每次启动编辑器程序时，`SessionManager` 会加载或创建新的 HTML 文件，并为其生成对应的编辑器（`HTMLEditor` 实例）。在一个会话中，可以同时打开多个文件，`SessionManager` 还负责保存文件、关闭文件、切换活动编辑器等工作。
- **HTMLEditor** 则专注于对 HTML 文件进行具体操作，比如插入元素、删除元素、修改元素的文本等。每个 HTML 文件都对应一个 `HTMLEditor` 实例，用户的编辑操作都通过该模块来实现。为了让用户的编辑过程更加顺畅，`HTMLEditor` 还实现了撤销和重做功能。每次用户执行操作时，系统会记录状态，以便后续的撤销和重做。
- **FileManager** 作为服务模块，为整个系统提供文件加载和保存服务，还可以根据用户需求以树状结构或者缩进结构的格式显示文件目录。这样用户可以直观地查看当前文件夹的组织情况，尤其是在多个文件的管理上显得更加友好。
- **HTMLDocument** 和 **HTMLElement** 共同构建了 HTML 文档的模型。`HTMLDocument` 代表一个完整的 HTML 文件，包括 `<html>`、`<head>`、`<body>` 等顶层结构，而 `HTMLElement` 则代表 HTML 文件中的每一个元素（标签）。这种设计不仅便于管理文档整体结构，也方便用户对每个元素进行操作，比如增删改查。
- ~~**状态管理**：为了记录每个文件的状态，系统引入了 `EditorState` 类。每个 `HTMLEditor` 实例都有对应的状态管理，记录了文件是否被修改、是否显示元素的 ID 等信息。在程序退出时，`SessionManager` 会将这些状态保存到一个 JSON 文件中，以便用户下次启动时可以继续上次的编辑。~~
- ~~**命令处理**：为了更好地处理用户在命令行中输入的各种操作，我们推荐使用 `CommandHandler` 模块。该模块会解析用户输入的命令，并调用相应的模块来完成操作，这样可以保持系统的松耦合性，并便于扩展新功能。~~

### 模块交互与设计模式

模块之间通过接口进行交互，每个模块的职责明确，确保各部分的独立性和可扩展性。

- **SessionManager 和 HTMLEditor 的交互**

  `SessionManager` 是用户与多个 `HTMLEditor` 实例之间的桥梁。每当用户加载一个新文件时，`SessionManager` 会创建一个新的 `HTMLEditor` 实例，并将其设置为当前活动的编辑器。所有对 HTML 文件的操作请求都通过 `SessionManager` 传递给具体的 `HTMLEditor`，比如插入元素、删除元素、修改文本等。这样，`SessionManager` 可以方便地在多个文件之间切换，用户也能够随时编辑不同的 HTML 文件。

- **命令模式的应用**

  项目中的每个编辑操作（比如插入、删除、修改）都被封装成了独立的命令对象，符合命令模式的设计思想。每个命令对象包含 `execute()` 和 `undo()` 方法，这样在执行某个命令时，不仅能完成操作，还能记录下来，以便需要时撤销操作。系统通过维护 `undo_stack` 和 `redo_stack` 两个堆栈来实现撤销和重做功能。每次执行操作后，命令对象会被推入 `undo_stack`，用户请求撤销时，就从 `undo_stack` 中弹出并执行 `undo()` 方法。

- **单一职责原则和工厂模式**

  项目严格遵循单一职责原则，每个模块只负责某一个方面的工作，例如 `HTMLEditor` 只处理 HTML 的具体操作，而 `FileManager` 只负责文件相关的操作。这样设计的好处是每个模块都很清晰，易于理解和维护。~~工厂模式的引入用来创建不同类型的 HTML 标签，减少重复的代码，并为后续扩展新的 HTML 元素类型提供便利。~~

  

没有图，缺点图。

## 3. 运行程序的环境配置

- **编程语言**：Python 3.8 及以上
- **依赖库**：
  - `beautifulsoup4==4.12.3`：用于解析和操作 HTML。
  - `pyspellchecker==0.8.1`：用于对文本内容进行拼写检查。
  - `setuptools==75.1.0`：用于安装和管理依赖。
  - `soupsieve==2.6`：用于辅助 `BeautifulSoup4` 进行解析。
  - `wheel==0.44.0`：用于构建 Python 包。

### 环境安装步骤
1. **克隆项目代码**：
   ```sh
   git clone git@github.com:JianxXiong/softwaredev.git
   cd softwaredev/lab1/code
   ```

2. **创建虚拟环境**（可选，但推荐）：
   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows 下为 venv\Scripts\activate
   ```

3. **安装依赖**：
   创建一个 `requirements.txt` 文件，并包含以下内容：
   ```
   beautifulsoup4==4.12.3
   pyspellchecker==0.8.1
   setuptools==75.1.0
   soupsieve==2.6
   wheel==0.44.0
   ```
   然后运行：
   ```sh
   pip install -r requirements.txt
   ```

### 运行程序
在项目根目录下运行以下命令来启动 HTML 编辑器：
```sh
cd lab1/code/
python main.py
```

该命令将启动多文件 HTML 编辑器，用户可以使用命令行交互进行文件的加载、编辑、保存等操作。

## 4. 支持的命令

编辑器提供了一系列命令，用户可以用这些命令来管理文件和对 HTML 内容进行编辑。以下是支持的命令和它们的功能：
- **文件管理命令**：
  - `load <filename>`：加载或创建一个新的 HTML 编辑器。
  - `save <filename>`：保存当前编辑器中的文件。
  - `close`：关闭当前编辑器，支持在关闭前保存文件。
  - `editor-list`：显示所有打开的编辑器，带有当前活动编辑器的标记。
  - `edit <filename>`：切换活动编辑器。
  - `showid true/false`：切换当前编辑器是否显示元素的 ID。
  - `dir-tree` / `dir-indent`：以树型或缩进格式显示文件目录。

- **编辑功能命令**：
  - `insert <tag> <id> <target_id> [content]`：在指定元素前插入新元素。
  - `append <tag> <id> <parent_id> [content]`：在指定父元素内添加新元素。
  - `edit-id <old_id> <new_id>`：修改元素的 ID。
  - `edit-text <element_id> [new_content]`：修改元素内部的文本。
  - `delete <element_id>`：删除指定元素。

- **其他功能**：
  - `undo` / `redo`：撤销或重做上一次操作。
  - `spell-check`：对文档中的文本进行拼写检查。
  - `print-tree` / `print-indent [indent]`：显示 HTML 结构，支持树形结构或缩进格式。
  - `help`：显示所有可用命令的帮助信息。
  - `exit`：退出程序并保存会话状态。

## 5. 使用实例
以下是编辑器的部分运行实例：

```sh
html-editor> load test.html
Loaded editor for test.html

html-editor> insert div new-div body "This is a new div"
Element inserted before 'body'.

html-editor> save test.html
Saved test.html

html-editor> editor-list
> test.html

html-editor> exit
Session saved. Exiting...
```

## 6. 自动测试
使用Python 的 unittest 为该项目编写了自动化测试脚本。

### 运行程序
在项目根目录下运行以下命令来启动自动化测试脚本：
```sh
cd lab1/code/
python autotest.py
```

该命令将启动自动化测试脚本，通过一系列函数调用和断言来测试项目功能。

## 7. 结论
本项目通过面向对象的设计，提供了一个功能全面的命令行 HTML 编辑器，支持多文件的加载、编辑和管理，同时实现了撤销和重做功能，增强了用户体验。项目的模块化设计使其更具可维护性和可扩展性，结合使用设计模式使代码更加优雅简洁。
