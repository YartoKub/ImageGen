import numpy as np
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from numpyimagevisualizer import ItemWidget
from PIL import Image

class UploadList(QWidget):
    def __init__(self, parent=None):
        super(UploadList, self).__init__(parent)
        self.setFixedHeight(700); 
        self.setFixedWidth(520); 
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #cfcfcf; padding: 0px; margin: 0px; border: none;")

        self.raw_photograph_list = []
        self.raw_normal_map_list = []
        self.raw_color_map_list = []
        self.raw_depth_map_list = []
        self.representatives = []
        
        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        for i in range(9):  
            item_widget = self.RandomWidget(i + 1)
            #self.scroll_area_layout.addWidget(item_widget)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def UpdateRepresentatives(self):
        for i in reversed(range(self.scroll_area_layout.count())):
            self.scroll_area_layout.itemAt(i).widget().setParent(None)

        for i in range(len(self.representatives)):
            self.scroll_area_layout.addWidget(self.representatives[i])
        
    
    def ItemSwap(self, some_item, diff):
        intA = self.representatives.index(some_item)
        intB = intA + diff
        print(f'Вверх {intA, intB}')
        if intA < 0 or intB < 0: return
        if intA >= len(self.representatives) or intB >= len(self.representatives): return

        self.representatives[intA], self.representatives[intB] = self.representatives[intB], self.representatives[intA]

        self.UpdateRepresentatives()

    def RandomWidget(self, item_num):
        data = np.random.rand(64, 64, 3) * 255
        data = data.astype(np.uint8)
        image = QImage(data, data.shape[1], data.shape[0], QImage.Format_RGB888)
        pixel_map = QPixmap.fromImage(image)
        new_item_widget = ItemWidget(self, item_num, pixel_map)
        self.representatives.append(new_item_widget)
        self.scroll_area_layout.addWidget(new_item_widget)
        return new_item_widget
    

    def AddNewWidget(self, new_numpy_image):
        data = new_numpy_image
        data = data.astype(np.uint8)
        image = QImage(data, data.shape[1], data.shape[0], QImage.Format_RGB888)
        pixel_map = QPixmap.fromImage(image)
        new_item_widget = ItemWidget(self, 0, pixel_map) # тут стоит ноль потому что он ничего не значит
        self.representatives.append(new_item_widget) 
        self.scroll_area_layout.addWidget(new_item_widget)
        return new_item_widget
    
# ============================ UPDATING ELEMENT CONTENTS ===============================================
    def FillElement(self, my_element):
        element_index = -1
        for i in range(len(self.representatives)):
            if self.representatives[i] == my_element:
                element_index = i
                break
        if element_index == -1: 
            print("Элемент в списке не найден")
            return

        print(element_index)

    def SingularUpdate():
        return

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

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    url = url.toLocalFile()
                    print(type(url))
                    if not self.IsTypeValid(url):
                        continue

                    new_img = Image.open(url)
                    np_array = np.asarray(new_img)
                    print(np_array.shape)

                    if not self.IsSizeValid(np_array):
                        continue
                    print(f"валидная ссылка: {str(url)}")
                    self.AddNewWidget(np_array)
                else:
                    continue
        else:
            event.ignore()

    def IsSizeValid(self, np_image):
        if np_image.shape != (64,64,3): # Вообще можно сделать просто "return np_image.shape != (64,64,3)", но тогда принта не будет
            print("Неправильная форма картинки: " + str(np_image.shape) + " нужна 64х64х3")
            return False
        return True
    
    def IsTypeValid(self, url):
        if not (url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg")):
            print("Плохой формат файла")
            return False
        return True


        



        