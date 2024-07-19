"""
程序主入口
"""
import sys

from PyQt5.QtWidgets import QApplication
from ui.index import Index

# 创建app
app = QApplication(sys.argv)
# 运行主页面
myWindow = Index()
myWindow.show()
# 退出
sys.exit(app.exec_())