import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

import cr


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pixmap = None
        self.ui = cr.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.openfile)
        # self.scene = QGraphicsScene()
        # self.ui.gV.setScene(self.scene)
        # self.ui.gV.setDragMode(QGraphicsView.ScrollHandDrag)
        self.ui.gV.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滚动条
        self.ui.gV.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平滚动条
        self.ui.gV.show()

    def openfile(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "open image files", "./", "Image files(*.jpg)")
        self.ui.gV.set_image(filename)
        # img = cv2.imread(filename, cv2.IMREAD_COLOR)
        # rec = img.shape
        # bytesPerLine = 3 * rec[1]
        # # print(img.data)
        # qimg = QImage(img.data, rec[1], rec[0], bytesPerLine, QImage.Format_BGR888)
        # self.scene.clear()
        # self.pixmap = QPixmap.fromImage(qimg)
        # self.scene.addPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
