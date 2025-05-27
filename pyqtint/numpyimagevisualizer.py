from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import numpy as np

from pyqtint.VectorInputField import VectorInput

NORMAL_MAP = 0
DEPTH_MAP = 1
COLOR_MAP = 2
PHOTOGRAPH_MAP = 3

IMAGE_VISUALIZER_IMAGE_SIZE = 64
IMAGE_VISUALIZER_BUTTON_WIDTH = 30
IMAGE_VISUALIZER_MARGIN = 5
IMAGE_VISUALIZER_SQUARE_BUTTON_H = 30
class ItemWidget(QListWidget):
    def __init__(self, my_parent, item_number, q_image):
        super().__init__()
        self.my_parent = my_parent
        self.setFixedWidth(IMAGE_VISUALIZER_IMAGE_SIZE * 4 + IMAGE_VISUALIZER_BUTTON_WIDTH * 2 + IMAGE_VISUALIZER_MARGIN * 2)
        self.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN * 2 + IMAGE_VISUALIZER_SQUARE_BUTTON_H)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gold;")

        self.vector_representation = VectorInput(IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE, IMAGE_VISUALIZER_BUTTON_WIDTH, self)
        self.vector_representation.move(IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_IMAGE_SIZE)

        self.photograph = QLabel(self)
        self.photograph.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 0,   IMAGE_VISUALIZER_MARGIN)
        self.photograph.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE)
        self.photograph.setFixedWidth (IMAGE_VISUALIZER_IMAGE_SIZE)
        self.photograph.setScaledContents(True)
        self.photograph.setPixmap(q_image)

        self.color_map = QLabel(self)
        self.color_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 1, IMAGE_VISUALIZER_MARGIN)
        self.color_map.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE)
        self.color_map.setFixedWidth (IMAGE_VISUALIZER_IMAGE_SIZE)
        self.color_map.setScaledContents(True)
        self.color_map.setPixmap        (QPixmap("ImageGen\\pyqtint\\placeholder_color.png"))

        self.normal_map = QLabel(self)
        self.normal_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 2, IMAGE_VISUALIZER_MARGIN)
        self.normal_map.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE)
        self.normal_map.setFixedWidth (IMAGE_VISUALIZER_IMAGE_SIZE)
        self.normal_map.setScaledContents(True)
        self.normal_map.setPixmap       (QPixmap("ImageGen\\pyqtint\\placeholder_normal.png"))

        self.depth_map = QLabel(self)
        self.depth_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 3, IMAGE_VISUALIZER_MARGIN)
        self.depth_map.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE)
        self.depth_map.setFixedWidth (IMAGE_VISUALIZER_IMAGE_SIZE)
        self.depth_map.setScaledContents(True)
        self.depth_map.setPixmap        (QPixmap("ImageGen\\pyqtint\\placeholder_depth.png"))

        self.print_button = QPushButton(self)
        self.print_button.setText(f'Log{item_number}')
        self.print_button.clicked.connect(self.print_message)
        self.print_button.setFixedWidth(30);  self.print_button.setFixedHeight(40);
        self.print_button.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 4,IMAGE_VISUALIZER_MARGIN)
        self.print_button.setStyleSheet("background-color: pink;")

        self.delete_button = QPushButton(self)
        self.delete_button.setText(f'Del{item_number}')
        self.delete_button.clicked.connect(self.delete_self)
        self.delete_button.setFixedWidth(30);  self.delete_button.setFixedHeight(20);
        self.delete_button.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 4, IMAGE_VISUALIZER_IMAGE_SIZE - 20 + IMAGE_VISUALIZER_MARGIN)
        self.delete_button.setStyleSheet("background-color: #d12913;")

        self.up_button   = QPushButton(self)
        self.up_button  .setText(f'^^^{item_number}')
        self.up_button  .clicked.connect(self.move_up)
        self.up_button  .setFixedWidth(30);  self.up_button.  setFixedHeight(30);
        self.up_button  .move(IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_MARGIN)
        self.up_button  .setStyleSheet("background-color: #6bc6cf;")

        self.down_button = QPushButton(self)
        self.down_button.setText(f'vvv{item_number}')
        self.down_button.clicked.connect(self.move_down)
        self.down_button.setFixedWidth(30);  self.down_button.setFixedHeight(30);
        self.down_button.move(IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN - IMAGE_VISUALIZER_SQUARE_BUTTON_H)
        self.down_button.setStyleSheet("background-color: #6bc6cf;")

        self.update_color = QPushButton(self)
        self.update_color.setText(f'color')
        self.update_color.clicked.connect(self.updateColor)
        self.update_color.setFixedWidth(IMAGE_VISUALIZER_IMAGE_SIZE);  
        self.update_color.setFixedHeight(IMAGE_VISUALIZER_SQUARE_BUTTON_H);
        self.update_color.move(IMAGE_VISUALIZER_IMAGE_SIZE * 1 + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN)
        self.update_color.setStyleSheet("background-color: #6bc6cf;")

        self.update_normal = QPushButton(self)
        self.update_normal.setText(f'normal')
        self.update_normal.clicked.connect(self.updateNormal)
        self.update_normal.setFixedWidth(IMAGE_VISUALIZER_IMAGE_SIZE);  
        self.update_normal.setFixedHeight(IMAGE_VISUALIZER_SQUARE_BUTTON_H);
        self.update_normal.move(IMAGE_VISUALIZER_IMAGE_SIZE * 2 + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN)
        self.update_normal.setStyleSheet("background-color: #6bc6cf;")

        self.update_depth = QPushButton(self)
        self.update_depth.setText(f'depth')
        self.update_depth.clicked.connect(self.updateDepth)
        self.update_depth.setFixedWidth(IMAGE_VISUALIZER_IMAGE_SIZE);  
        self.update_depth.setFixedHeight(IMAGE_VISUALIZER_SQUARE_BUTTON_H);
        self.update_depth.move(IMAGE_VISUALIZER_IMAGE_SIZE * 3 + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_MARGIN, IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN)
        self.update_depth.setStyleSheet("background-color: #6bc6cf;")
    
    def updateNormal(self):
        self.my_parent.SingularUpdate(self, "NORMAL")
        self.fullUpdate()
    def updateColor(self):
        self.my_parent.SingularUpdate(self, "COLOR")
        self.fullUpdate()
    def updateDepth(self):
        self.my_parent.SingularUpdate(self, "DEPTH")
        self.fullUpdate()
    
    def updateVector(self, new_value):
        self.my_parent.updateVector(self, new_value)
        
    def print_message(self):
        self.my_parent.FillElement(self)

    def delete_self(self):
        self.my_parent.deleteElement(self)

    def move_up(self):
        self.my_parent.ItemSwap(self, -1)

    def move_down(self):
        self.my_parent.ItemSwap(self, 1)

    def fullUpdate(self):
        element_id = self.my_parent.representativeIndex(self)
        print(element_id)
        photo_raw = self.my_parent.raw_photograph_list[element_id]
        photo_raw = (photo_raw * 255).astype(np.uint8)
        photo = QImage(photo_raw, photo_raw.shape[1], photo_raw.shape[0], QImage.Format_RGB888)
        self.photograph.setPixmap(QPixmap.fromImage(photo))

        color_raw = self.my_parent.raw_color_map_list[element_id] 
        color_raw = (color_raw * 255).astype(np.uint8)
        color = QImage(color_raw, color_raw.shape[1], color_raw.shape[0], QImage.Format_RGB888)
        self.color_map.setPixmap(QPixmap.fromImage(color))

        normal_raw = self.my_parent.raw_normal_map_list[element_id] 
        normal_raw = (normal_raw * 255).astype(np.uint8)
        normal = QImage(normal_raw, normal_raw.shape[1], normal_raw.shape[0], QImage.Format_RGB888)
        self.normal_map.setPixmap(QPixmap.fromImage(normal))

        depth_raw = self.my_parent.raw_depth_map_list[element_id] 
        depth_raw = (depth_raw * 255).astype(np.uint8)
        depth = QImage(depth_raw, depth_raw.shape[1], depth_raw.shape[0], QImage.Format_RGB888)
        self.depth_map.setPixmap(QPixmap.fromImage(depth))

        #print("FULL UPDATE COMMENECED")

    def update_self(self, map_id, new_numpy_image):
        image = QImage(new_numpy_image, new_numpy_image.shape[1], new_numpy_image.shape[0], QImage.Format_RGB888)
        if map_id == NORMAL_MAP: self.normal_map.setPixmap(image)
        elif map_id == DEPTH_MAP: self.depth_map.setPixmap(image)
        elif map_id == COLOR_MAP: self.color_map.setPixmap(image)
        elif map_id == PHOTOGRAPH_MAP: self.photograph.setPixmap(image)
        else: return

        return
