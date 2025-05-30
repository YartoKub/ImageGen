import numpy as np
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image

from pyqtint.numpyimagevisualizer import ItemWidget


class UploadList(QWidget):
    def __init__(self, parent=None):
        super(UploadList, self).__init__(parent)
        self.setFixedHeight(700); 
        self.setFixedWidth(64 * 8 + 100); 
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #cfcfcf; padding: 0px; margin: 0px; border: none;")
        self.setContentsMargins(0, 0, 0, 0)

        self.my_parent = parent
        self.raw_photograph_list = []
        self.raw_normal_map_list = []
        self.raw_color_map_list = []
        self.raw_depth_map_list = []

        self.raw_diffuse_list = []
        self.raw_specular_list = []
        self.raw_shadow_list = []
        self.raw_result_list = []

        self.raw_vector_list = []

        self.representatives = []
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.scroll_area.setAlignment(Qt.AlignLeft | Qt.AlignTop)
# Это нужно отключить чтобы работало
        #dummy_list = ["ImageGen\\pyqtint\\Dummies\\0016.png", "ImageGen\\pyqtint\\Dummies\\0079.png", "ImageGen\\pyqtint\\Dummies\\3117.png", "ImageGen\\pyqtint\\Dummies\\0016.png", "ImageGen\\pyqtint\\Dummies\\0079.png", "ImageGen\\pyqtint\\Dummies\\3117.png"]
        #for i in range(len(dummy_list)):  
        #    new_img = Image.open(dummy_list[i])
        #    np_array = np.asarray(new_img)
        #    item_widget = self.AddNewWidget(np_array)
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
        self.raw_vector_list[intA], self.raw_vector_list[intB] = self.raw_vector_list[intB], self.raw_vector_list[intA]

        self.raw_photograph_list[intA], self.raw_photograph_list[intB] = self.raw_photograph_list[intB], self.raw_photograph_list[intA]
        self.raw_normal_map_list[intA], self.raw_normal_map_list[intB] = self.raw_normal_map_list[intB], self.raw_normal_map_list[intA]
        self.raw_depth_map_list[intA], self.raw_depth_map_list[intB] = self.raw_depth_map_list[intB], self.raw_depth_map_list[intA]
        self.raw_color_map_list[intA], self.raw_color_map_list[intB] = self.raw_color_map_list[intB], self.raw_color_map_list[intA]

        self.raw_diffuse_list[intA], self.raw_diffuse_list[intB] = self.raw_diffuse_list[intB], self.raw_diffuse_list[intA]
        self.raw_specular_list[intA], self.raw_specular_list[intB] = self.raw_specular_list[intB], self.raw_specular_list[intA]
        self.raw_shadow_list[intA], self.raw_shadow_list[intB] = self.raw_shadow_list[intB], self.raw_shadow_list[intA]
        self.raw_result_list[intA], self.raw_result_list[intB] = self.raw_result_list[intB], self.raw_result_list[intA]

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

        self.raw_photograph_list.append(new_numpy_image / 255) # деление для нормализации от 0-255 к 0-1
        self.raw_normal_map_list.append(new_numpy_image / 255)
        self.raw_color_map_list.append(new_numpy_image / 255)
        self.raw_depth_map_list.append(new_numpy_image / 255)

        self.raw_diffuse_list.append(new_numpy_image / 255)
        self.raw_specular_list.append(new_numpy_image / 255)
        self.raw_shadow_list.append(new_numpy_image / 255)
        self.raw_result_list.append(new_numpy_image / 255)

        self.raw_vector_list.append(np.array([0,0,0]))

        self.scroll_area_layout.addWidget(new_item_widget)
        new_item_widget.fullUpdate()
        return new_item_widget
    
# ============================ UPDATING ELEMENT CONTENTS ===============================================
    def updateVector(self, element, new_value):
        element_id = self.representativeIndex(element)
        self.raw_vector_list[element_id] = new_value

    def representativeIndex(self, my_element):
        for i in range(len(self.representatives)):
            if self.representatives[i] == my_element:
                return i
        return -1
                
    def deleteElement(self, my_element):
        element_index = self.representativeIndex(my_element)
        self.representatives.pop(element_index)
        self.raw_photograph_list.pop(element_index)
        self.raw_normal_map_list.pop(element_index)
        self.raw_color_map_list.pop(element_index)
        self.raw_depth_map_list.pop(element_index)

        self.raw_diffuse_list.pop(element_index)
        self.raw_specular_list.pop(element_index)
        self.raw_shadow_list.pop(element_index)
        self.raw_result_list.pop(element_index)

        self.raw_vector_list.pop(element_index)
        my_element.setParent(None)  
        my_element.deleteLater()

    def FillElement(self, my_element):
        element_index = self.representativeIndex(my_element)
        if element_index == -1: 
            print("Элемент в списке не найден")
            return

        print(element_index)

    def SingularUpdate(self, my_element, map_name): # Какие-то макароны получаются, надо как нибудь переписать используя систему Event-ов
        element_id = self.representativeIndex(my_element)
        '''
        element_to_give = self.raw_photograph_list[element_id]
        addition1 = None; addition2 = None
        if map_name =="DIFFUSE": 
            element_to_give = self.raw_normal_map_list[element_id]
            addition1 = self.raw_depth_map_list[element_id]
        if map_name=="SPECULAR": 
            element_to_give = self.raw_normal_map_list[element_id]
            addition1 = self.raw_depth_map_list[element_id]
        if map_name == "SHADOW": 
            element_to_give = self.raw_depth_map_list [element_id]
        if map_name == "LIGHT": 
            element_to_give = self.raw_diffuse_list [element_id]
            addition1       = self.raw_specular_list[element_id]
            addition2       = self.raw_shadow_list  [element_id]
        '''
        vector_to_give = self.raw_vector_list[element_id]
        print(element_id, map_name)
        element_received = self.my_parent.SingularUpdate(element_id, map_name, vector_to_give) # uint8 0-255
        if map_name == "NORMAL": self.raw_normal_map_list[element_id] = element_received
        if map_name == "COLOR" : self.raw_color_map_list [element_id] = element_received
        if map_name == "DEPTH" : self.raw_depth_map_list [element_id] = element_received
        if map_name =="DIFFUSE": self.raw_diffuse_list   [element_id] = element_received
        if map_name=="SPECULAR": self.raw_specular_list  [element_id] = element_received
        if map_name == "SHADOW": self.raw_shadow_list    [element_id] = element_received
        if map_name == "LIGHT" : self.raw_result_list    [element_id] = element_received
        

    def MassUpdate(self, map_name):
        results = self.my_parent.MassUpdate(map_name)

        if map_name == "NORMAL": 
            for i in range(results.shape[0]):
                self.raw_normal_map_list[i] = results[i]
        if map_name == "COLOR" : 
            for i in range(results.shape[0]):
                self.raw_color_map_list[i] = results[i]
        if map_name == "DEPTH" :
            for i in range(results.shape[0]):
                self.raw_depth_map_list[i] = results[i]
        if map_name == "DIFFUSE": 
            for i in range(results.shape[0]):
                self.raw_diffuse_list[i] = results[i]
        if map_name == "SPECULAR": 
            for i in range(results.shape[0]):
                self.raw_specular_list[i] = results[i]
        if map_name == "SHADOW": 
            for i in range(results.shape[0]):
                self.raw_shadow_list[i] = results[i]
        if map_name == "LIGHT" : 
            for i in range(results.shape[0]):
                self.raw_result_list[i] = results[i]

        for i in range(len(self.representatives)):
            self.representatives[i].fullUpdate()

    def simpleFullUpdate(self):
        for i in range(len(self.representatives)):
            self.representatives[i].fullUpdate()
            
        #return element_received

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


        



        