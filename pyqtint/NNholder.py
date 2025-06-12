import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap

from pyqtint.ScrollableLabel import ScrollLabel
from pyqtint.numpyimagevisualizer import ItemWidget

NN_PRESET_ROLES = {
    "NORMAL": ("#d399ff", "ImageGen\\pyqtint\\placeholder_normal.png", "Normal map", 0),
    "COLOR" : ("#8adb96", "ImageGen\\pyqtint\\placeholder_color.png" , "Color map" , 1),
    "DEPTH" : ("#c2c2c2", "ImageGen\\pyqtint\\placeholder_depth.png" , "Depth map" , 2),
    "LIGHT" : ("#fcfcd2", "ImageGen\\pyqtint\\placeholder_depth.png" , "Light map" , 3),
}
class NNHolder(QWidget):
    def __init__(self, parent=None, preset_role = "LIGHT", my_array = None):
        super(NNHolder, self).__init__(parent)
        self.my_parent = parent
        my_color, my_default_adress, my_label_text, my_index = NN_PRESET_ROLES[preset_role]
        self.my_role = preset_role
        self.setFixedHeight(180); 
        self.setFixedWidth(80); 
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {my_color};")

        self.example_image = QLabel(self)
        self.example_image.move(8,2)
        self.example_image.setFixedHeight(64)
        self.example_image.setFixedWidth (64)
        self.example_image.setScaledContents(True)
        if my_array != None: 
            self.example_image.setPixmap       (QPixmap(my_array[my_index]))

        self.map_label = QLabel(self)
        self.map_label.move(0, 66)
        self.map_label.setFixedHeight(20)
        self.map_label.setFixedWidth (80)
        self.map_label.setText(my_label_text)
        self.map_label.setAlignment(Qt.AlignCenter)

        self.status_label = ScrollLabel(self)
        self.status_label.move(0, 84)
        self.status_label.setFixedHeight(80)
        self.status_label.setFixedWidth (80)
        self.status_label.setText(" no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded ")
        self.status_label.setAttribute(Qt.WA_StyledBackground, True)
        self.status_label.setStyleSheet(f"background-color: #cf1d1d;")

        self.clear_button = QPushButton(self)
        self.clear_button.setText(f' CLEAR ')
        self.clear_button.clicked.connect(self.modelClear)
        self.clear_button.setFixedWidth(80);  
        self.clear_button.setFixedHeight(16);
        self.clear_button.move(0, 164)
        self.clear_button.setStyleSheet("background-color: gold;")
    
# ============================ MMY CONTENTS ===========================================================
    def modelUpdate(self, status, reason_str):
        if status == True:
            self.loadSuccess(reason_str)
        if status == False:
            self.loadFailed(reason_str)

    def loadFailed(self, reason_str):
        self.status_label.setText(reason_str)
        self.status_label.setStyleSheet("background-color: #cf1d1d;")
        self.example_image.setPixmap       (QPixmap(NN_PRESET_ROLES[self.my_role][1]))

    def loadSuccess(self, reason_str):
        self.status_label.setText(reason_str)
        self.status_label.setStyleSheet("background-color: #1dcf41;")

    def modelClear(self):
        self.my_parent.modelClear(self.my_role)
        self.status_label.setText("Model cleared")
        self.status_label.setStyleSheet("background-color: #cf1d1d;")

# ============================ DRAGGING AND LOADING ===================================================
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls: event.accept()
        else: event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            if len(event.mimeData().urls()) != 1:
                event.ignore()
                return
            url = event.mimeData().urls()[0]
            if not url.isLocalFile():
                event.ignore()
                return
            
            url = url.toLocalFile()
            if not self.IsTypeValid(url):
                return
            self.my_parent.LoadModel(self.my_role, url)
            

        else:
            event.ignore()

    def IsTypeValid(self, url):
        if not url.endswith(".keras"):
            print("Плохой формат файла")
            return False
        return True
