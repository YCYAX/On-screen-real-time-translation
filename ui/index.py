import cv2
from PIL.Image import Image
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
import mss
import numpy
import ctypes
class Index(QWidget):
    def __init__(self):
        super().__init__()
        self.high = int(1920 * 0.5)
        self.width = int(1080 * 0.5)
        # screen
        self.screen = None
        #
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.ui()

    def ui(self):
        self.resize(self.high, self.width)
        self.setWindowTitle("屏幕实时翻译")
        # top栏
        self.top_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.top_layout)
        # down栏
        self.down_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.down_layout)
        # function
        self.areaButton = QPushButton("翻译页面选取")
        self.areaButton.clicked.connect(self.selectArea)
        self.top_layout.addWidget(self.areaButton)
        self.showImage = QLabel()
        self.down_layout.addWidget(self.showImage)

    def selectArea(self):
        # get screen size
        user32 = ctypes.windll.user32
        screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        # set screen monitor
        monitor = {"top": 0, "left": 0, "width": screen_size[0], "height": screen_size[1]}
        # get screen
        with mss.mss() as image:
            self.screen = numpy.array(image.grab(monitor))
        # show image
        pixmap = QPixmap(img)
        self.showImage.setPixmap(pixmap)


