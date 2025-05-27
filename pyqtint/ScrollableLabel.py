import numpy as np
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QVBoxLayout, QPushButton, QListWidget, QFrame
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image

from pyqtint.numpyimagevisualizer import ItemWidget

class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        #self.setContentsMargins(0, 0, 0, 0)

        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        lay.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)
        self.label.setStyleSheet("padding: 2px; margin: 0px; border: none;")
        #self.label.setContentsMargins(0, 0, 0, 0)

    def setText(self, text):
        self.label.setText(text)