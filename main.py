import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListView, QListWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from pyqtint.DragDrop import ListBoxWidget
from PyQt5.QtCore import Qt, QUrl
import os

from pyqtint.numpyimage import UploadList
from pyqtint.NNholder import NNHolder
from pyqtint.NN_manager import NN_Manager
from pyqtint.massActions import MassActions
from pyqtint.volumeGIF import VolumeGIF
from pyqtint.my_face import MyFace
from pyqtint.vectorParser import VectorParser
from pyqtint.settingsPanel import SettingsPanel
from pyqtint.finalGIF import FinalGIF
# Высота 720, ширина: 1280. Мне некогда делать тянущийся интерфейс
SECOND_COLUMN = 1280 - 592 - 210 - 100
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("ImageGen - изменение освещения")
        self.setGeometry(0, 0, 1280, 720)
        self.setContentsMargins(0, 0, 0, 0)

        self.nn_manager = NN_Manager(self)

        self.randlist_label = QtWidgets.QLabel(self)
        self.randlist_label.setText("=== Drag & Drop ===")
        self.randlist_label.setAlignment(Qt.AlignCenter)
        self.randlist_label.setStyleSheet("background-color: #6bc6cf; padding: 0px; margin: 0px; border: none;")
        self.randlist_label.move(80,0); self.randlist_label.setFixedHeight(30); self.randlist_label.setFixedWidth(592 + 20)

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

        self.volumeGIF = VolumeGIF(self,  self.randlist)
        self.volumeGIF.move(1280 - 210, 150)

        self.mass_actions = MassActions(SECOND_COLUMN, 30, self,  self.randlist)
        self.mass_actions.move(592 + 100, 150)

        THE_GRUMPY_ARRAY = [
            resource_path("ImageGen\\pyqtint\\Dummies\\simply_me.png"),
            resource_path("ImageGen\\pyqtint\\Dummies\\churchill.png"),
            resource_path("ImageGen\\pyqtint\\Dummies\\bladerunner.png")
            ]

        self.my_face = MyFace(self, 210, 150, THE_GRUMPY_ARRAY)
        self.my_face.move(1280 - 210, 0)

        self.big_parser = VectorParser(SECOND_COLUMN, 150, self, self.randlist)
        self.big_parser.move(592 + 100, 0)

        self.settings = SettingsPanel(SECOND_COLUMN, 360, self)
        self.settings.move(592 + 100, 180)

        self.finalGIFmaker = FinalGIF(210, 480, self, self.randlist)
        self.finalGIFmaker.move(1280 - 210, 372)

        self.nn_manager.databank = self.randlist
        self.nn_manager.settings = self.settings

    

    def LoadModel(self, model_map, model_adress):
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

    def modelClear(self, model_map):
        if model_map == "NORMAL":
            self.nn_manager.NORMAL_MODEL = None
        if model_map == "COLOR" :
            self.nn_manager.COLOR_MODEL = None
        if model_map == "DEPTH" :
            self.nn_manager.DEPTH_MODEL = None
        if model_map == "LIGHT" :
            self.nn_manager.LIGHT_MODEL = None
        
    
    def SingularUpdate(self, my_element, map_name, vector):
        return self.nn_manager.RenderSingleImage(map_name, my_element, vector)
    
    def MassUpdate(self, map_name):
        return self.nn_manager.RenderMultipleImages(map_name)

def application():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    application()



