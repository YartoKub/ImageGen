from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

NORMAL_MAP = 0
DEPTH_MAP = 1
COLOR_MAP = 2
PHOTOGRAPH_MAP = 3

IMAGE_VISUALIZER_IMAGE_SIZE = 100
IMAGE_VISUALIZER_BUTTON_WIDTH = 30
IMAGE_VISUALIZER_MARGIN = 5
IMAGE_VISUALIZER_SQUARE_BUTTON_H = 30
class ItemWidget(QListWidget):
    def __init__(self, my_parent, item_number, q_image):
        super().__init__()
        self.my_parent = my_parent
        self.setFixedWidth(460)
        self.setFixedHeight(IMAGE_VISUALIZER_IMAGE_SIZE + IMAGE_VISUALIZER_MARGIN * 2)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gold;")

        self.photograph = QLabel(self)
        self.photograph.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 0,   IMAGE_VISUALIZER_MARGIN)
        self.photograph.setFixedHeight(100)
        self.photograph.setFixedWidth (100)
        self.photograph.setScaledContents(True)
        self.photograph.setPixmap(q_image)

        self.color_map = QLabel(self)
        self.color_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 1, IMAGE_VISUALIZER_MARGIN)
        self.color_map.setFixedHeight(100)
        self.color_map.setFixedWidth (100)
        self.color_map.setScaledContents(True)
        self.color_map.setPixmap        (QPixmap("ImageGen\\pyqtint\\placeholder_color.png"))

        self.normal_map = QLabel(self)
        self.normal_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 2, IMAGE_VISUALIZER_MARGIN)
        self.normal_map.setFixedHeight(100)
        self.normal_map.setFixedWidth (100)
        self.normal_map.setScaledContents(True)
        self.normal_map.setPixmap       (QPixmap("ImageGen\\pyqtint\\placeholder_normal.png"))

        self.depth_map = QLabel(self)
        self.depth_map.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 3, IMAGE_VISUALIZER_MARGIN)
        self.depth_map.setFixedHeight(100)
        self.depth_map.setFixedWidth (100)
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
        self.delete_button.move(IMAGE_VISUALIZER_MARGIN + IMAGE_VISUALIZER_BUTTON_WIDTH + IMAGE_VISUALIZER_IMAGE_SIZE * 4,80 + IMAGE_VISUALIZER_MARGIN)
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
        

    def print_message(self):
        self.my_parent.FillElement(self)

    def delete_self(self):
        self.setParent(None)  
        self.deleteLater()

    def move_up(self):
        self.my_parent.ItemSwap(self, -1)

    def move_down(self):
        self.my_parent.ItemSwap(self, 1)

    def update_self(self, map_id, new_numpy_image):
        image_to_change = None
        if map_id == NORMAL_MAP: image_to_change = self.normal_map
        elif map_id == DEPTH_MAP: image_to_change = self.depth_map
        elif map_id == COLOR_MAP: image_to_change = self.color_map
        elif map_id == PHOTOGRAPH_MAP: image_to_change = self.photograph
        else: return

        image = QImage(new_numpy_image, new_numpy_image.shape[1], new_numpy_image.shape[0], QImage.Format_RGB888)
        image_to_change.setPixmap(image)
        return
