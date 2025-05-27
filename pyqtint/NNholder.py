import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from numpyimagevisualizer import ItemWidget
from ScrollableLabel import ScrollLabel
NN_PRESET_ROLES = {
    "NORMAL": ("#d399ff", "ImageGen\\pyqtint\\placeholder_normal.png", "Normal map"),
    "COLOR" : ("#8adb96", "ImageGen\\pyqtint\\placeholder_color.png" , "Color map" ),
    "DEPTH" : ("#c2c2c2", "ImageGen\\pyqtint\\placeholder_depth.png" , "Depth map" ),
    "LIGHT" : ("#fcfcd2", "ImageGen\\pyqtint\\placeholder_depth.png" , "Light map" ),
}
class NNHolder(QWidget):
    def __init__(self, parent=None, preset_role = "LIGHT"):
        super(NNHolder, self).__init__(parent)
        self.my_parent = parent
        my_color, my_default_adress, my_label_text = NN_PRESET_ROLES[preset_role]
        self.my_role = preset_role
        self.setFixedHeight(180); 
        self.setFixedWidth(80); 
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {my_color};")

        self.example_image = QLabel(self)
        self.example_image.move(8,8)
        self.example_image.setFixedHeight(64)
        self.example_image.setFixedWidth (64)
        self.example_image.setScaledContents(True)
        self.example_image.setPixmap       (QPixmap(my_default_adress))

        self.map_label = QLabel(self)
        self.map_label.move(0, 72)
        self.map_label.setFixedHeight(20)
        self.map_label.setFixedWidth (80)
        self.map_label.setText(my_label_text)
        self.map_label.setAlignment(Qt.AlignCenter)

        self.status_label = ScrollLabel(self)
        self.status_label.move(0, 90)
        self.status_label.setFixedHeight(80)
        self.status_label.setFixedWidth (80)
        self.status_label.setText(" no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded  no model loaded ")
        self.status_label.setAttribute(Qt.WA_StyledBackground, True)
        self.status_label.setStyleSheet(f"background-color: #cf1d1d;")
    
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
            print("начинаю грузить модель в NN holder")
            self.my_parent.LoadModel(self.my_role, url)
            

        else:
            event.ignore()

    def IsTypeValid(self, url):
        if not url.endswith(".keras"):
            print("Плохой формат файла")
            return False
        return True
