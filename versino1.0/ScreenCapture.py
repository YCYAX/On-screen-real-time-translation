import cv2

import mss

import numpy as np


class ScreenCapture:
    """

  parameters

  ----------

    screen_resolution : Tuple[int, int]

      屏幕宽高，分别为x，y

    capture_region : Tuple[float, float]

      实际截图范围，分别为x，y，(1.0, 1.0)表示全屏检测，越低检测范围越小(始终保持屏幕中心为中心)

    window_name : str

      显示窗口名

    exit_code : int

      结束窗口的退出键值，为键盘各键对应的ASCII码值，默认是ESC键

  """

    def __init__(self, screen_resolution=(1920, 1080), capture_region=(0.5, 0.5), window_name='test', exit_code=0x1B):
        self.screen_capture = mss.mss()  # 实例化mss，并使用高效模式

        self.screen_width = screen_resolution[0]  # 屏幕的宽

        self.screen_height = screen_resolution[1]  # 屏幕的高

        self.capture_region = capture_region  # 捕获区域

        self.screen_center_x, self.screen_center_y = self.screen_width // 2, self.screen_height // 2  # 屏幕中心点坐标

        # 截图区域

        self.capture_width, self.capture_height = int(self.screen_width * self.capture_region[0]), int(

            self.screen_height * self.capture_region[1])  # 宽高

        self.capture_left, self.capture_top = int(

            0 + self.screen_width // 2 * (1. - self.capture_region[0])), int(

            0 + self.screen_height // 2 * (1. - self.capture_region[1]))  # 原点

        self.display_window_width, self.display_window_height = self.screen_width // 3, self.screen_height // 3  # 显示窗口大小

        self.monitor_settings = {

            'left': self.capture_left,

            'top': self.capture_top,

            'width': self.capture_width,

            'height': self.capture_height

        }

        self.window_name = window_name

        self.exit_code = exit_code

        self.img = None

    def grab_screen_mss(self, monitor=None):
        if monitor is None:
            monitor = self.monitor_settings

        # cap.grab截取图片，np.array将图片转为数组，cvtColor将BRGA转为BRG,去掉了透明通道

        # cv2.cvtColor(np.array(self.screen_capture.grab(monitor)), cv2.COLOR_BGRA2BGR)
        return cv2.cvtColor(np.array(self.screen_capture.grab(monitor)), cv2.COLOR_BGRA2BGR)
