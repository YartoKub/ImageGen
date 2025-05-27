from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QMovie

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class VolumeGIF(QWidget):
    def __init__(self, my_parent, image_holder):
        super(VolumeGIF, self).__init__(my_parent)
        self.my_parent = my_parent
        self.image_holder = image_holder
        self.setFixedWidth(210)
        self.setFixedHeight(230)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: gold;")

        self.update_normal = QPushButton(self)
        self.update_normal.setText(f'GIF объема')
        self.update_normal.clicked.connect(self.regenerateMovie)
        self.update_normal.setFixedWidth(210);  
        self.update_normal.setFixedHeight(20);
        self.update_normal.setStyleSheet("background-color: red;")

        self.label = QLabel(self)
        self.label.setFixedWidth(200)
        self.label.setFixedHeight(200)
        self.label.move(5, 5 + 20)
        self.label.setObjectName("label")
        self.label.setScaledContents(True)

        #self.movie = QMovie("ImageGen\\pyqtint\\Dummies\\height0_5.gif")
        #self.label.setMovie(self.movie)
        #self.movie.start()
    
    def regenerateMovie(self):
        my_photos = self.image_holder.raw_photograph_list
        my_depths = self.image_holder.raw_depth_map_list

        length = len(my_photos)
        degree_change = 90 / length
        my_frames1 = [getDepthGraph(my_photos[i], my_depths[i], 5, degree_change * i) for i in range(length)]
        sec_length = length - 1
        my_frames2 = [getDepthGraph(my_photos[sec_length - i], my_depths[sec_length - i], 5, degree_change * (sec_length - i)) for i in range(sec_length)]
        
        my_frames1 = my_frames1 + my_frames2
        my_frames1 = np.array(my_frames1)
        images_array = my_frames1.astype(np.uint8)
        images = []
        for img in images_array:
            images.append(Image.fromarray(img).resize((192, 192)))

        images[0].save('depthanimation.gif',
                    save_all=True,
                    append_images=images[1:],
                    duration=100, 
                    loop=0)
        
        self.movie = QMovie("depthanimation.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
    
    
def getDepthGraph(photo, depth, cam_z = 5, rotation = 10):
    width_px = 512 
    height_px = 512  
    dpi = 128 
    figsize = (width_px / dpi, height_px / dpi)
    ax = plt.figure(figsize=figsize, dpi=dpi).add_subplot(projection='3d')
    
    colors = photo
    width = photo.shape[0]
    height= photo.shape[1]
    x = np.repeat(np.arange(width), height)
    y = np.tile(np.arange(height), width)
    
    depths = depth[:, :, 0].flatten() * 64
    
    ax.scatter(xs=depths, ys=x, zs=y, c=colors.reshape(-1, 3))
    
    ax.set_xlim(0, 63)
    ax.set_ylim(0, 63)
    ax.set_zlim(0, 63)

    ax.view_init(elev=cam_z, azim=-rotation, roll=0)
    
    plt.axis('off')
    plt.tight_layout()
    
    fig = plt.gcf()
    fig.canvas.draw()
    
    image_array = np.frombuffer(fig.canvas.buffer_rgba (), dtype=np.uint8)
    image_array = image_array.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    
    plt.close(fig)
    return image_array[:,:,0:3] # тут массив имеет 4 канала, я возвращаю только 3 т.к. прозрачногсть не нужна