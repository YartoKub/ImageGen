import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListView, QListWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from DragDrop import ListBoxWidget
from PyQt5.QtCore import Qt, QUrl
from numpyimage import UploadList

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("прострая прога")
        self.setGeometry(100, 100, 600, 700)

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(500, 10)
        self.btn.setText("Нажимабельно")
        self.btn.setFixedWidth(150)


        self.logoLabel = QtWidgets.QLabel(self)
        self.logoLabel.setFixedHeight(100)
        self.logoLabel.setFixedWidth(100)
        self.logoLabel.setScaledContents(True)
        self.logoLabel.move(500,100)

        self.pixmap = QPixmap('ImageGen\\pyqtint\\arrowpower.png')
        self.logoLabel.setPixmap(self.pixmap)

        self.randlist_label = QtWidgets.QLabel(self)
        self.randlist_label.setText("=== Drag & Drop ===")
        self.randlist_label.setAlignment(Qt.AlignCenter)
        self.randlist_label.setStyleSheet("background-color: #6bc6cf; padding: 0px; margin: 0px; border: none;")
        self.randlist_label.move(0,0); self.randlist_label.setFixedHeight(30); self.randlist_label.setFixedWidth(520)

        self.randlist = UploadList(self)
        self.randlist.move(0, 30)


def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()

