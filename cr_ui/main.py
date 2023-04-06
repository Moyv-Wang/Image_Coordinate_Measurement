import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
from PyQt5 import uic

import cr


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Dialog")
        self.resize(379, 173)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(60, 30, 291, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(60, 60, 261, 16))
        self.label_3.setObjectName("label_3")
        self.widget = QWidget(self)
        self.widget.setGeometry(QRect(60, 100, 225, 26))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2.setText("若标志点带有点号，程序会自动检测，若")
        self.label_3.setText( "检测结果不正确请自行输入：")
        self.label.setText( "点号：")
        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setGeometry(QRect(280, 140, 93, 28))
        self.confirmBtn.setText("确定")
        self.confirmBtn.setObjectName("confirmBtn")

        self.horizontalLayout.addWidget(self.confirmBtn)
        self.confirmBtn.setDefault(True)  # 设置为默认按钮
        self.confirmBtn.clicked.connect(self.accept)  # 点击按钮触发accept方法

        # self.diaui = uic.loadUi("numDialog.ui")
        # self.diaui.confirmBtn.setDefault(True)
        # self.diaui.setWindowModality(Qt.ApplicationModal)
        # self.diaui.confirmBtn.clicked.connect(self.accept)

    # def handle_slot(self):
    #     sender = self.sender()
    #     text = sender.get_text()
    #     self.diaui.lineEdit.setText(text)
    #     self.diaui.exec_()


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

        self.dialog = MyDialog()
        self.ui.gV.rectSelected.connect(self.dialog.exec)

    def openfile(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "open image files", "./", "Image files(*.jpg)")
        # print(filename + "null")
        if filename != "":
            self.ui.gV.set_image(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
