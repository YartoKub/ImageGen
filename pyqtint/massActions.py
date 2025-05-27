import numpy as np
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image

from pyqtint.numpyimagevisualizer import ItemWidget

class MassActions(QWidget):
    def __init__(self, parent=None, image_holder = None):
        super(MassActions, self).__init__(parent)
        self.my_parent = parent
        self.image_holder = image_holder
        self.setFixedHeight(30); 
        self.setFixedWidth(1280 - 440 - 80); 
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: #cfcfcf;")

        self.update_depth = QPushButton(self)
        self.update_depth.setText(f'all depth')
        self.update_depth.clicked.connect(self.GenerateAllDepths)
        self.update_depth.setFixedWidth(60);  
        self.update_depth.setFixedHeight(30);
        self.update_depth.move(0, 0 )
        self.update_depth.setStyleSheet("background-color: #6bc6cf;")

        self.update_normal = QPushButton(self)
        self.update_normal.setText(f'all normals')
        self.update_normal.clicked.connect(self.GenerateAllNormals)
        self.update_normal.setFixedWidth(60);  
        self.update_normal.setFixedHeight(30);
        self.update_normal.move(60, 0 )
        self.update_normal.setStyleSheet("background-color: #6bc6cf;")

        self.update_color = QPushButton(self)
        self.update_color.setText(f'all colors')
        self.update_color.clicked.connect(self.GenerateAllColors)
        self.update_color.setFixedWidth(60);  
        self.update_color.setFixedHeight(30);
        self.update_color.move(120, 0 )
        self.update_color.setStyleSheet("background-color: #6bc6cf;")

    def GenerateAllNormals(self):
        self.image_holder.MassUpdate("NORMAL")
        return
    def GenerateAllColors(self):
        self.image_holder.MassUpdate("COLOR")
        return
    def GenerateAllDepths(self):
        self.image_holder.MassUpdate("DEPTH")
        return
    
