import time 
import win32gui
import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
import sys

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.show()

class Timer(object):
    def __init__(self) -> None:
        self.start_timestamp = time.time()
        self.durtion = 0

    def record(self, reset=True):
        self.durtion = round(1000 * (time.time() - self.start_timestamp))
        if reset:
            self.start_timestamp = time.time()

    def __str__(self) -> str:
        return f'耗时: {self.durtion} ms'

hwnd_title = {}

def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

win32gui.EnumWindows(get_all_hwnd, 0)
print(hwnd_title)
hwnd = 0
for key, value in hwnd_title.items():
    if "文件" in value:
        hwnd = key
        print(hwnd, value)
        break

app = QApplication(sys.argv)
window = MainWidget()
window.show()

screen = QApplication.primaryScreen()

timer = Timer()
for _ in range(10):
    qimg = screen.grabWindow(hwnd).toImage()
    shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    shape += (4, )
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    img = np.array(ptr, dtype=np.uint8).reshape(shape)
    timer.record()
    print(timer, img.shape)
cv2.imwrite('test.png', img)

sys.exec(app.exec())
