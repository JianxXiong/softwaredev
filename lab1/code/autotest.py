import os
import json
import shutil
import unittest
from unittest.mock import patch, mock_open
from model.html_editor import HTMLEditor
from model.file_manager import FileManager
from model.session_manager import SessionManager

class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = 'temp_test_dir'
        os.makedirs(self.temp_dir, exist_ok=True)
        os.chdir(self.temp_dir)
        self.test_file = 'test.html'
        with open(self.test_file, 'w') as f:
            f.write('<html><head><title>Test</title></head><body><h1>Test</h1></body></html>')
        self.session = SessionManager()

    def tearDown(self):
        # 清理临时目录和文件
        os.chdir('..')
        shutil.rmtree('temp_test_dir', ignore_errors=True)

    def test_load_session_state(self):
        # 创建一个模拟的session_state.json文件
        session_data = {
            "files": [self.test_file],
            "active_editor": self.test_file,
            "showid": {self.test_file: False}
        }
        with open('session_state.json', 'w') as f:
            json.dump(session_data, f)
        # 重新初始化SessionManager以加载会话状态
        session = SessionManager()
        self.assertIn(self.test_file, session.editors)
        self.assertEqual(session.active_editor, self.test_file)
        self.assertFalse(session.showid[self.test_file])

    def test_load_editor(self):
        # 加载一个新的编辑器
        new_file = 'new_test.html'
        with open(new_file, 'w') as f:
            f.write('<html><body><p>New Test</p></body></html>')
        self.session.load_editor(new_file)
        self.assertIn(new_file, self.session.editors)
        self.assertEqual(self.session.active_editor, new_file)

    #还有问题
    def test_save_editor(self):
        # Modify editor content and save
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        #editor.document.head.title.content = 'Modified Title'
        editor.edit_element_content('head', 'Modified Test')
        self.session.save_editor(self.test_file)
        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertIn('<head id="head">Modified Test', content)

    def test_close_editor(self):
        # 关闭编辑器
        self.session.load_editor(self.test_file)
        self.session.close_editor()
        self.assertNotIn(self.test_file, self.session.editors)
        self.assertIsNone(self.session.active_editor)

    def test_switch_editor(self):
        new_file = 'new_test.html'
        with open(new_file, 'w') as f:
            f.write('<html><body><p>New Test</p></body></html>')
        self.session.load_editor(new_file)
        self.session.edit_switch(self.test_file)
        self.assertEqual(self.session.active_editor, self.test_file)

    def test_set_showid(self):
        self.session.load_editor(self.test_file)
        self.session.set_showid(False)
        self.assertFalse(self.session.showid[self.test_file])

    def test_dir_display(self):
        # 显示目录结构
        with patch('builtins.print') as mock_print:
            self.session.dir_display(style="tree")
            mock_print.assert_called()

    def test_insert_element(self):
        # 插入元素
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.insert_before('h1', 'new_id', 'new_tag', 'New Content')
        self.assertIn('new_id', editor.document.get_element_ids())

    def test_append_element(self):
        # 追加元素
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.add_into('body', 'new_id', 'New Content', 'p')
        self.assertIn('new_id', editor.document.get_element_ids())

    def test_edit_element_id(self):
        # 编辑元素ID
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.edit_element_id('h1', 'new_h1')
        self.assertNotIn('h1', editor.document.get_element_ids())
        self.assertIn('new_h1', editor.document.get_element_ids())

    def test_edit_element_content(self):
        # 编辑元素内容
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.edit_element_content('h1', 'Modified Content')
        self.assertIn('Modified Content', editor.document.get_element_content('h1'))

    def test_delete_element(self):
        # 删除元素
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.delete_element('h1')
        self.assertNotIn('h1', editor.document.get_element_ids())

    def test_undo_redo(self):
        # 撤销和重做
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        editor.edit_element_content('h1', 'Modified Content')
        editor.undo()
        self.assertNotIn('Modified Content', editor.document.get_element_content('h1'))
        editor.redo()
        self.assertIn('Modified Content', editor.document.get_element_content('h1'))

    def test_spell_check(self):
        self.session.load_editor(self.test_file)
        editor = self.session.editors[self.test_file]
        # 拼写检查（mock拼写检查器）
        with patch('model.html_document.HTMLDocument.check_spelling') as mock_check:
            editor.check_spelling()
            mock_check.assert_called()

    def test_print_tree(self):
        # 打印树结构
        with patch('builtins.print') as mock_print:
            self.session.load_editor(self.test_file)
            self.session.editors[self.test_file].print_tree()
            mock_print.assert_called()

    def test_print_indent(self):
        # 打印缩进格式
        with patch('builtins.print') as mock_print:
            self.session.load_editor(self.test_file)
            self.session.editors[self.test_file].print_indent(2)
            mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()