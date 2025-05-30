import numpy as np
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
from matplotlib import pyplot as plt

THE_GRUMPY_ARRAY = [
    "ImageGen\\pyqtint\\Dummies\\simply_me.png",
    "ImageGen\\pyqtint\\Dummies\\churchill.png", 
    "ImageGen\\pyqtint\\Dummies\\bladerunner.png"
    ]

class MyFace(QPushButton):
    def __init__(self, my_parent, width, height, grumpy_array):
        super(MyFace, self).__init__(my_parent)
        self.grumpy_array = grumpy_array
        self.my_parent = my_parent
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.current_me = 0

        self.my_label = QLabel(self)
        self.my_label.setAttribute(Qt.WA_StyledBackground, True)
        self.my_label.setStyleSheet("background-color: gold;")
        self.my_label.setScaledContents(True)
        self.my_label.setFixedWidth(210)
        self.my_label.setFixedHeight(150)
        self.my_label.setPixmap(QPixmap(self.grumpy_array[self.current_me]))
        self.clicked.connect(self.scrollMe)

    def scrollMe(self):
        self.current_me = (self.current_me + 1) % len(self.grumpy_array)
        self.my_label.setPixmap(QPixmap(self.grumpy_array[self.current_me]))
