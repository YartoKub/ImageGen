import numpy as np
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import re

class VectorInput(QLineEdit):
    def __init__(self, width, heigth, parent=None):
        super(VectorInput, self).__init__(parent)
        self.my_parent = parent
        self.setMaxLength(20)
        self.setAlignment(Qt.AlignLeft)
        self.setFixedHeight(heigth); 
        self.setFixedWidth(width); 
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #cf6d6d;")
        self.textChanged.connect(self.onTextChange)

    def onTextChange(self):
        if re.search(r'[^-0-9., ]', self.text()): 
            #print("bad bad")
            self.badVector()
            return 
        
        parts = self.text().split(",")
        if len(parts) != 3: 
            #print("not enouyght parts")
            self.badVector()
            return 
        
        new_vector = np.array([0,0,0], np.float32)
        try: # try except в разы проще чем вручную проверять корректность строки
            new_vector[0] = float(parts[0])
            new_vector[1] = float(parts[1])
            new_vector[2] = float(parts[2])
            self.goodVector(new_vector)
        except:
            self.badVector()
        

    def goodVector(self, new_value):
        self.setStyleSheet("background-color: #6dcf87;")
        self.my_parent.updateVector(new_value)

    def badVector(self):
        self.setStyleSheet("background-color: #cf6d6d;")
        self.my_parent.updateVector(np.array([0.0,0.0,0.0]))
        #self.my_parent.updateVector()
    