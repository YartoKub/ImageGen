import numpy as np
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image

LENGTH_UPDATE = [48, 58, 48, 56, 62, 58, 45]


class MassActions(QWidget):
    def __init__(self, width, heigth, parent=None, image_holder = None):
        super(MassActions, self).__init__(parent)
        self.my_parent = parent
        self.image_holder = image_holder
        self.setFixedHeight(heigth); 
        self.setFixedWidth(width); 
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: #cfcfcf;")

        self.update_color = QPushButton(self)
        self.update_color.setText(f'all colors')
        self.update_color.clicked.connect(self.GenerateAllColors)
        self.update_color.setFixedWidth(LENGTH_UPDATE[0]);  
        self.update_color.setFixedHeight(30);
        self.update_color.move(0, 0 )
        self.update_color.setStyleSheet("background-color: #6bc6cf;")

        self.update_normal = QPushButton(self)
        self.update_normal.setText(f'all normals')
        self.update_normal.clicked.connect(self.GenerateAllNormals)
        self.update_normal.setFixedWidth(LENGTH_UPDATE[1]);  
        self.update_normal.setFixedHeight(30);
        self.update_normal.move(LENGTH_UPDATE[0], 0 )
        self.update_normal.setStyleSheet("background-color: #6bc6cf;")
        
        self.update_depth = QPushButton(self)
        self.update_depth.setText(f'all depth')
        self.update_depth.clicked.connect(self.GenerateAllDepths)
        self.update_depth.setFixedWidth(LENGTH_UPDATE[2]);  
        self.update_depth.setFixedHeight(30);
        self.update_depth.move(LENGTH_UPDATE[0] + LENGTH_UPDATE[1], 0 )
        self.update_depth.setStyleSheet("background-color: #6bc6cf;")

        self.update_diffuse = QPushButton(self)
        self.update_diffuse.setText(f'all diffuse')
        self.update_diffuse.clicked.connect(self.GenerateAllDiffuse)
        self.update_diffuse.setFixedWidth(LENGTH_UPDATE[3]);  
        self.update_diffuse.setFixedHeight(30);
        self.update_diffuse.move(LENGTH_UPDATE[0] + LENGTH_UPDATE[1] + LENGTH_UPDATE[2], 0 )
        self.update_diffuse.setStyleSheet("background-color: #6bc6cf;")

        self.update_specular = QPushButton(self)
        self.update_specular.setText(f'all specular')
        self.update_specular.clicked.connect(self.GenerateAllSpecular)
        self.update_specular.setFixedWidth(LENGTH_UPDATE[4]);  
        self.update_specular.setFixedHeight(30);
        self.update_specular.move(LENGTH_UPDATE[0] + LENGTH_UPDATE[1] + LENGTH_UPDATE[2] + LENGTH_UPDATE[3], 0 )
        self.update_specular.setStyleSheet("background-color: #6bc6cf;")

        self.update_shadow = QPushButton(self)
        self.update_shadow.setText(f'all shadow')
        self.update_shadow.clicked.connect(self.GenerateAllShadow)
        self.update_shadow.setFixedWidth(LENGTH_UPDATE[5]);  
        self.update_shadow.setFixedHeight(30);
        self.update_shadow.move(LENGTH_UPDATE[0] + LENGTH_UPDATE[1] + LENGTH_UPDATE[2] + LENGTH_UPDATE[3] + LENGTH_UPDATE[4], 0 )
        self.update_shadow.setStyleSheet("background-color: #6bc6cf;")

        self.update_light = QPushButton(self)
        self.update_light.setText(f'all light')
        self.update_light.clicked.connect(self.GenerateAllLight)
        self.update_light.setFixedWidth(LENGTH_UPDATE[6]);  
        self.update_light.setFixedHeight(30);
        self.update_light.move(LENGTH_UPDATE[0] + LENGTH_UPDATE[1] + LENGTH_UPDATE[2] + LENGTH_UPDATE[3] + LENGTH_UPDATE[4] + LENGTH_UPDATE[5], 0 )
        self.update_light.setStyleSheet("background-color: #6bc6cf;")

    def GenerateAllNormals(self):
        self.image_holder.MassUpdate("NORMAL")
        return
    def GenerateAllColors(self):
        self.image_holder.MassUpdate("COLOR")
        return
    def GenerateAllDepths(self):
        self.image_holder.MassUpdate("DEPTH")
        return
    def GenerateAllDiffuse(self):
        self.image_holder.MassUpdate("DIFFUSE")
        return
    def GenerateAllSpecular(self):
        self.image_holder.MassUpdate("SPECULAR")
        return
    def GenerateAllShadow(self):
        self.image_holder.MassUpdate("SHADOW")
        return
    def GenerateAllLight(self):
        self.image_holder.MassUpdate("LIGHT")
        return
    
