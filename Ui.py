import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from guiyeujiexi.parse_104 import parse_message_104
from guiyeujiexi.parse_101 import parse_message_101
from PyQt6.QtGui import QIcon

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".") # 当前工作目录的路径

    return os.path.normpath(os.path.join(base_path, relative_path)) # 返回实际路径

# 自定义输出流类
class EmittingStream(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # 只有当 text 不只是换行符时才追加
        if text != '\n':
            self.text_widget.append(text)

    def flush(self):
        pass

# PyQt 应用的主类
class AppDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.protocol = ""

        # 设置窗口初始大小
        self.setGeometry(1000, 100, 720, 950)

        # 设置窗口图标
        icon_path = get_path(r'UI\basketball.ico')
        self.setWindowIcon(QIcon(icon_path))

        # 使用QUiLoader加载UI文件
        loader = uic.loadUi
        ui_path = get_path(r'UI\zijianUI.ui')
        self.ui = loader(ui_path)
        self.setCentralWidget(self.ui)
        # 连接按钮的点击事件到槽函数
        self.ui.pushButton.clicked.connect(self.parse_message)

        # 连接信号与槽
        self.ui.comboBox.currentTextChanged.connect(self.handle_combobox_change)

        # 重定向 print 输出到文本框
        sys.stdout = EmittingStream(self.ui.shuchukuang)

    def handle_combobox_change(self, text):
        if text == "GB104":
            self.protocol = "104"
        elif text == "GB101(平衡)":
            self.protocol = "101"
        elif text == "GB101(非平衡)":
            self.protocol = "101F"

    def parse_message(self):
        # 清空上一次的输出
        self.ui.shuchukuang.clear()

        # 获取输入并进行解析
        message = self.ui.shurukuang.toPlainText()

        # 如果用户未选择规约类型，弹出警告框
        if not self.protocol:
            QMessageBox.warning(self, "警告", "未选择规约类型")
            return
        elif self.protocol == "104":
            transmode = 0
            parse_message_104(message, transmode)

        elif self.protocol == "101":
            transmode = 2
            parse_message_101(message, transmode)

        elif self.protocol == "101F":
            transmode = 1
            parse_message_101(message, transmode)


# 主程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec())  # 启动事件循环
