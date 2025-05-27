import numpy as np
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import re

class VectorInput(QLineEdit):
    def __init__(self, width, heigth, parent=None):
        super(VectorInput, self).__init__(parent)
        self.my_parent = parent
        self.setMaxLength(15)
        self.setAlignment(Qt.AlignLeft)
        self.setFixedHeight(heigth); 
        self.setFixedWidth(width); 
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #cf6d6d;")
        self.textChanged.connect(self.onTextChange)

    def onTextChange(self):
        if re.search(r'[^0-9., ]', self.text()): 
            self.badVector()
            return 
        
        parts = self.text().split(",")
        if len(parts) != 3: 
            self.badVector()
            return 
        
        new_vector = np.array([0,0,0], np.float32)

        for i in range(3):
            if parts[i].strip() == ".":
                self.badVector()
                return
            
            dot_counter = 0
            for symbol in parts[i]:
                if symbol == ".":
                    dot_counter += 1
            if dot_counter > 1: 
                self.badVector()
                return
            new_vector[i] = float(parts[i]) if (parts[i].strip() != "") else 0.0

        print(new_vector[0], new_vector[1], new_vector[2])
        self.goodVector(new_vector)

    def goodVector(self, new_value):
        self.setStyleSheet("background-color: #6dcf87;")
        self.my_parent.updateVector(new_value)

    def badVector(self):
        self.setStyleSheet("background-color: #cf6d6d;")
        #self.my_parent.updateVector()