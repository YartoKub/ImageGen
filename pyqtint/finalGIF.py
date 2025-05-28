from PyQt5.QtWidgets import QWidget,  QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

import numpy as np
from PIL import Image
import os

class FinalGIF(QWidget):
    def __init__(self, width, heigth, my_parent, image_holder):
        super(FinalGIF, self).__init__(my_parent)
        self.my_parent = my_parent
        self.image_holder = image_holder
        self.setFixedWidth(width)
        self.setFixedHeight(heigth)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gold;")

        self.generate_gif = QPushButton(self)
        self.generate_gif.setText(f'GIF анимация')
        self.generate_gif.clicked.connect(self.regenerateMovie)
        self.generate_gif.setFixedWidth(210);  
        self.generate_gif.setFixedHeight(20);
        self.generate_gif.setStyleSheet("background-color: red;")

        self.label = QLabel(self)
        self.label.setFixedWidth(192)
        self.label.setFixedHeight(192)
        self.label.move(5, 5 + 20)
        self.label.setObjectName("label")
        self.label.setScaledContents(True)

        self.file_loc = QTextEdit(self)
        self.file_loc.setFixedWidth(200)
        self.file_loc.setFixedHeight(80)
        self.file_loc.move(5, 5 + 200 + 10 + 5)
        self.file_loc.setWordWrapMode(True)
        self.file_loc.setText("")
        self.file_loc.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.dump_images = QPushButton(self)
        self.dump_images.setText(f'Сохранить все картинки')
        self.dump_images.clicked.connect(self.dumpAllImages)
        self.dump_images.setFixedWidth(200);  
        self.dump_images.setFixedHeight(20);
        self.dump_images.setStyleSheet("background-color: red;")
        self.dump_images.move(5, 200 + 100 + 5)

    def dumpAllImages(self):
        photos = self.image_holder.raw_photograph_list
        normals = self.image_holder.raw_normal_map_list
        colors = self.image_holder.raw_color_map_list
        depth = self.image_holder.raw_depth_map_list

        diffs = self.image_holder.raw_diffuse_list
        specs = self.image_holder.raw_specular_list
        shadows = self.image_holder.raw_shadow_list
        results = self.image_holder.raw_result_list

        photos  = np.concatenate(photos, axis=0)
        normals = np.concatenate(normals, axis=0)
        colors  = np.concatenate(colors, axis=0)
        depth   = np.concatenate(depth, axis=0)

        diffs   = np.concatenate(diffs, axis=0)
        specs   = np.concatenate(specs, axis=0)
        shadows = np.concatenate(shadows, axis=0)
        results = np.concatenate(results, axis=0)

        dumpy = np.concatenate([photos, normals, colors, depth, diffs, specs, shadows, results], axis=1)
        dumpy = (dumpy * 255).astype(np.uint8)
        image = Image.fromarray(dumpy)
        my_name = 'all_frames.png'
        image.save(my_name)
        full_path = os.path.join(os.getcwd(), my_name)
        self.file_loc.setText(full_path)

    def regenerateMovie(self):
        my_photos = self.image_holder.raw_result_list

        length = len(my_photos)
        my_frames1 = [my_photos[i] for i in range(length)]
        sec_length = length - 1
        my_frames2 = [my_photos[sec_length - i] for i in range(sec_length)]
        
        my_frames1 = my_frames1 + my_frames2
        my_frames1 = np.array(my_frames1)
        images_array = (my_frames1 * 255).astype(np.uint8)
        images = []
        for img in images_array:
            images.append(Image.fromarray(img).resize((192, 192)))

        filename = 'finalanimation.gif'
        images[0].save(filename,
                    save_all=True,
                    append_images=images[1:],
                    duration=100, 
                    loop=0)
        
        current_directory = os.getcwd() 
        full_path = os.path.join(current_directory, filename)
        self.file_loc.setText(full_path)

        self.movie = QMovie(filename)
        self.label.setMovie(self.movie)
        self.movie.start()