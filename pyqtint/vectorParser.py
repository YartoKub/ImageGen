import numpy as np
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import re

BADCOLOR = "#cf6d6d"
GOODCOLOR = "#6dcf87"
CLASSIC_VALUES = [("x.xx", "y.yy", "z.zz"), ("x", "y", "z"), ("-x.xx", "-y.yy", "-z.zz")]
class VectorParser(QWidget):
    def __init__(self, width, heigth, parent=None, vector_storage=None):
        super(VectorParser, self).__init__(parent)
        self.my_parent = parent
        self.vector_storage = vector_storage
        self.setFixedHeight(heigth); 
        self.setFixedWidth(width); 
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gold")

        self.start_encapsulator = QLineEdit(self)
        self.start_encapsulator.setMaxLength(6)
        self.start_encapsulator.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.start_encapsulator.setAttribute(Qt.WA_StyledBackground, True)
        self.start_encapsulator.setStyleSheet(f"background-color: white")
        self.start_encapsulator.move(40, 5)
        self.start_encapsulator.setFixedWidth(30)
        self.start_encapsulator.setFixedHeight(30)

        self.end_encapsulator = QLineEdit(self)
        self.end_encapsulator.setMaxLength(6)
        self.end_encapsulator.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.end_encapsulator.setAttribute(Qt.WA_StyledBackground, True)
        self.end_encapsulator.setStyleSheet(f"background-color: white")
        self.end_encapsulator.move(75, 5)
        self.end_encapsulator.setFixedWidth(30)
        self.end_encapsulator.setFixedHeight(30)

        self.encapsulator = QLabel(self)
        self.encapsulator.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.encapsulator.setAttribute(Qt.WA_StyledBackground, True)
        self.encapsulator.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.encapsulator.move(5, 5)
        self.encapsulator.setFixedWidth(30)
        self.encapsulator.setFixedHeight(30)
        self.encapsulator.setText("(...)")

        self.inner_separator = QLineEdit(self)
        self.inner_separator.setMaxLength(6)
        self.inner_separator.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.inner_separator.setAttribute(Qt.WA_StyledBackground, True)
        self.inner_separator.setStyleSheet(f"background-color: white")
        self.inner_separator.move(50, 40)
        self.inner_separator.setFixedWidth(55)
        self.inner_separator.setFixedHeight(30)

        self.inner_separator_label = QLabel(self)
        self.inner_separator_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.inner_separator_label.setAttribute(Qt.WA_StyledBackground, True)
        self.inner_separator_label.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.inner_separator_label.move(5, 40)
        self.inner_separator_label.setFixedWidth(40)
        self.inner_separator_label.setFixedHeight(30)
        self.inner_separator_label.setText("x, y, z")
        
        self.main_input = QTextEdit(self)
        #self.main_input.setMaxLength(400)
        self.main_input.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_input.setAttribute(Qt.WA_StyledBackground, True)
        self.main_input.setStyleSheet("background-color: gold; padding: 3px")
        self.main_input.move(110, 5)
        self.main_input.setFixedWidth(width - 110 - 5)
        self.main_input.setFixedHeight(100)
        self.main_input.setWordWrapMode(True)

        self.down_button = QPushButton(self)
        self.down_button.setText(f' submit ')
        self.down_button.clicked.connect(self.parseBigString)
        self.down_button.setFixedWidth(65);  self.down_button.setFixedHeight(30);
        self.down_button.move(width - 65 - 5, 115)
        self.down_button.setStyleSheet("background-color: gold;")

        self.example_label = QLabel(self)
        self.example_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.example_label.setAttribute(Qt.WA_StyledBackground, True)
        self.example_label.setStyleSheet(f"background-color: white")
        self.example_label.move(5, 115)
        self.example_label.setFixedWidth(width - 5 - 70)
        self.example_label.setFixedHeight(30)

        self.caution_label = QLabel(self)
        self.caution_label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.caution_label.setAttribute(Qt.WA_StyledBackground, True)
        self.caution_label.setStyleSheet(f"background-color: white; font-size: 10px")
        self.caution_label.setWordWrap(True)
        self.caution_label.move(5, 75)
        self.caution_label.setFixedWidth(100)
        self.caution_label.setFixedHeight(35)
        self.caution_label.setText("Избегайте пробелов в (...) и x, y, z" )

        self.start_encapsulator.textChanged.connect(self.symbolFieldUpdate)
        self.start_encapsulator.setText("(")
        self.end_encapsulator.textChanged.connect(self.symbolFieldUpdate)
        self.end_encapsulator.setText(")")
        self.inner_separator.textChanged.connect(self.symbolFieldUpdate)
        self.inner_separator.setText(",")
        self.symbolFieldUpdate()

    def symbolFieldUpdate(self):
        enc_s = self.start_encapsulator.text()
        enc_e = self.end_encapsulator.text()
        inner_s = self.inner_separator.text()
        string_to_return = ""
        
        for x in range(3):
            values = CLASSIC_VALUES[x]
            local_string = values[0] + inner_s + values[1] + inner_s + values[2]
            string_to_return = string_to_return +  enc_s + local_string + enc_e 

        self.example_label.setText(string_to_return)
    
    def parseBigString(self):
        big_string = self.main_input.toPlainText()
        inn_s = self.inner_separator.text()
        enc_s = self.start_encapsulator.text()
        enc_e = self.end_encapsulator.text()
        try:
            capsules = []
            while len(big_string.strip()) > 0:
                #print(big_string)
                #print(len(big_string.strip()))
                start, end = self.find_capsule(big_string, enc_s, enc_e)
                #print(start, end, big_string[start], big_string[end])

                if start == -1 or end == -1:
                    self.failVectors()
                    return

                capsule = big_string[start + len(enc_s):end]
                big_string = big_string[end + len(enc_e):]

                capsule = capsule.split(inn_s)
                if len(capsule) != 3:
                    self.failVectors()
                    return

                c1 = float(capsule[0].strip())
                c2 = float(capsule[1].strip())
                c3 = float(capsule[2].strip())
                capsule = (c1, c2, c3)
                capsules.append(capsule)

            capsules = np.array(capsules)
            
        except:
            self.failVectors()
            return
        print(capsules)
        self.submitVectors(capsules) 
        return

    def failVectors(self):
        self.main_input.setStyleSheet(f"background-color: #ffcfcf")
        return
    
    def submitVectors(self, vectors):
        vector_list_length = len(self.vector_storage.raw_vector_list)
        limit = min(len(vectors), vector_list_length)
        for i in range(limit):
            self.vector_storage.raw_vector_list[i] = vectors[i]
        self.main_input.setStyleSheet(f"background-color: white")
        self.vector_storage.simpleFullUpdate()

    def find_capsule(self, vector_string, enc_s, enc_e):
        start = vector_string.find(enc_s)
        end = vector_string.find(enc_e)
        return start, end