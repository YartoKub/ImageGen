import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListView, QListWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from DragDrop import ListBoxWidget
from PyQt5.QtCore import Qt, QUrl
from numpyimage import UploadList
from NNholder import NNHolder
from NN_manager import NN_Manager
# Высота 720, ширина: 1280. Мне некогда делать тянущийся интерфейс
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("прострая прога")
        self.setGeometry(0, 0, 1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.nn_manager = NN_Manager(self)

        self.randlist_label = QtWidgets.QLabel(self)
        self.randlist_label.setText("=== Drag & Drop ===")
        self.randlist_label.setAlignment(Qt.AlignCenter)
        self.randlist_label.setStyleSheet("background-color: #6bc6cf; padding: 0px; margin: 0px; border: none;")
        self.randlist_label.move(80,0); self.randlist_label.setFixedHeight(30); self.randlist_label.setFixedWidth(520)

        self.randlist = UploadList(self)
        self.randlist.move(80, 30)

        self.nnh_normal = NNHolder(self, "NORMAL")
        self.nnh_normal.move(0, 0)
        self.nnh_color = NNHolder(self, "COLOR")
        self.nnh_color.move(0, 180)
        self.nnh_depth = NNHolder(self, "DEPTH")
        self.nnh_depth.move(0, 360)
        self.nnh_light = NNHolder(self, "LIGHT")
        self.nnh_light.move(0, 540)

    def LoadModel(self, model_map, model_adress):
        print("начинаю грузить модель в main")
        self.nn_manager.changeModel(model_map, model_adress)

    def modelUpdate(self, model_map, status, reason_str):
        if model_map == "NORMAL":
            self.nnh_normal.modelUpdate(status, reason_str)
        if model_map == "COLOR" :
            self.nnh_color .modelUpdate(status, reason_str)
        if model_map == "DEPTH" :
            self.nnh_depth .modelUpdate(status, reason_str)
        if model_map == "LIGHT" :
            self.nnh_light .modelUpdate(status, reason_str)

def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()

