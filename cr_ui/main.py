import sys
import csv

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
# from PyQt5 import uic

import cr
import tencent_ocr as ocr


class MyDialog(QDialog):
    confirm_sig = pyqtSignal()

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
        self.label_3.setText("检测结果不正确请自行输入：")
        self.label.setText("点号：")
        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setGeometry(QRect(180, 140, 93, 28))
        self.confirmBtn.setObjectName("confirmBtn")
        self.confirmBtn.setText("确定")
        self.confirmBtn.setDefault(True)  # 设置为默认按钮

        self.cancelBtn = QPushButton(self)
        self.cancelBtn.setGeometry(QRect(280, 140, 93, 28))
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.setText("取消")

        self.confirmBtn.clicked.connect(self.accept_record)  # 点击按钮触发accept方法
        self.cancelBtn.clicked.connect(self.accept)
        # self.confirmBtn.clicked.connect(lambda: self.confirm_btn_clicked.emit())

    def accept_record(self):
        self.confirm_sig.emit()
        self.accept()

    def popup(self):
        self.confirmBtn.setDefault(True)
        base64_data = ocr.image_to_base64("sub_pic.jpg")
        detected_text = ocr.tencentOCR(base64_data)
        self.lineEdit.setText(detected_text)
        self.exec()
        return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.y = None
        self.x = None
        self.pixmap = None
        self.ui = cr.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.openfile)
        self.ui.actionSave.triggered.connect(self.export_table_to_text)
        self.ui.gV.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭垂直滚动条
        self.ui.gV.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关闭水平滚动条
        self.ui.gV.show()

        self.dialog = MyDialog()
        self.dialog.confirm_sig.connect(self.get_res)
        self.ui.gV.rectSelected.connect(self.dialog.popup)

    def openfile(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "open image files", "./", "Image files(*.jpg)")
        # print(filename + "null")
        if filename != "":
            self.ui.gV.set_image(filename)
            self.ui.statusBar.showMessage("导入完成")

    def get_res(self):
        self.x, self.y = self.ui.gV.get_coordinate()
        rowPosition = self.ui.tW.rowCount()
        self.ui.tW.insertRow(rowPosition)

        # 设置该行的每个单元格内容
        num = self.dialog.lineEdit.text()
        self.ui.tW.setItem(rowPosition, 0, QTableWidgetItem(num))
        self.ui.tW.setItem(rowPosition, 1, QTableWidgetItem(str(self.x)))
        self.ui.tW.setItem(rowPosition, 2, QTableWidgetItem(str(self.y)))

    def export_table_to_text(self):
        with open("res.csv", 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["点号", "x", "y"])
            for row in range(self.ui.tW.rowCount()):
                row_data = []
                for column in range(self.ui.tW.columnCount()):
                    item = self.ui.tW.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                writer.writerow(row_data)
                self.ui.statusBar.showMessage("文件导出完成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
