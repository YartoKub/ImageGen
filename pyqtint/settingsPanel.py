import numpy as np
import cv2
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QVBoxLayout, QPushButton, QListWidget, QLineEdit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
from pyqtint.massActions import MassActions

GOODCOLOR = "#6dcf87"
BADCOLOR  = "#cf6d6d"
class SettingsPanel(QWidget):
    def __init__(self, width, heigth, parent=None):
        super(SettingsPanel, self).__init__(parent)
        self.my_parent = parent
        self.setFixedHeight(heigth); 
        self.setFixedWidth(width); 
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: #cfcfcf;")

        self.issues = True

        self.diffuse = QLabel(self)
        self.diffuse.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.diffuse.setAttribute(Qt.WA_StyledBackground, True)
        self.diffuse.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.diffuse.move(5, 5)
        self.diffuse.setFixedWidth(75)
        self.diffuse.setFixedHeight(30)
        self.diffuse.setText("Light Strength")

        self.light_power = QLineEdit(self)
        self.light_power.setMaxLength(8)
        self.light_power.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.light_power.setAttribute(Qt.WA_StyledBackground, True)
        self.light_power.setStyleSheet(f"background-color: {BADCOLOR}")
        self.light_power.move(85, 5)
        self.light_power.setFixedWidth(75)
        self.light_power.setFixedHeight(30)
        self.light_power.textChanged.connect(self.lightPowerCheck)

        self.specular = QLabel(self)
        self.specular.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.specular.setAttribute(Qt.WA_StyledBackground, True)
        self.specular.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.specular.move(5, 40)
        self.specular.setFixedWidth(90)
        self.specular.setFixedHeight(30)
        self.specular.setText("Specular Color")

        self.spec_color = QLineEdit(self)
        self.spec_color.setMaxLength(8)
        self.spec_color.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.spec_color.setAttribute(Qt.WA_StyledBackground, True)
        self.spec_color.setStyleSheet(f"background-color: {BADCOLOR}")
        self.spec_color.move(100, 40)
        self.spec_color.setFixedWidth(75)
        self.spec_color.setFixedHeight(30)
        self.spec_color.textChanged.connect(self.specularColorCheck)

        self.specular_f = QLabel(self)
        self.specular_f.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.specular_f.setAttribute(Qt.WA_StyledBackground, True)
        self.specular_f.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.specular_f.move(5, 75)
        self.specular_f.setFixedWidth(90)
        self.specular_f.setFixedHeight(30)
        self.specular_f.setText("Specular Factor")

        self.spec_factor = QLineEdit(self)
        self.spec_factor.setMaxLength(8)
        self.spec_factor.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.spec_factor.setAttribute(Qt.WA_StyledBackground, True)
        self.spec_factor.setStyleSheet(f"background-color: {BADCOLOR}")
        self.spec_factor.move(100, 75)
        self.spec_factor.setFixedWidth(75)
        self.spec_factor.setFixedHeight(30)
        self.spec_factor.textChanged.connect(self.specularFactorCheck)

        self.volume_threshhold_l = QLabel(self)
        self.volume_threshhold_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_threshhold_l.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_threshhold_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.volume_threshhold_l.move(5, 110)
        self.volume_threshhold_l.setFixedWidth(120)
        self.volume_threshhold_l.setFixedHeight(30)
        self.volume_threshhold_l.setText("Volume Threshhold")

        self.volume_threshhold = QLineEdit(self)
        self.volume_threshhold.setMaxLength(8)
        self.volume_threshhold.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_threshhold.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_threshhold.setStyleSheet(f"background-color: {BADCOLOR}")
        self.volume_threshhold.move(130, 110)
        self.volume_threshhold.setFixedWidth(75)
        self.volume_threshhold.setFixedHeight(30)
        self.volume_threshhold.textChanged.connect(self.volumeThreshholdCheck)

        self.volume_column_l = QLabel(self)
        self.volume_column_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_column_l.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_column_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.volume_column_l.move(5, 145)
        self.volume_column_l.setFixedWidth(120)
        self.volume_column_l.setFixedHeight(30)
        self.volume_column_l.setText("Column (слабое)")

        self.volume_column = QLineEdit(self)
        self.volume_column.setMaxLength(8)
        self.volume_column.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_column.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_column.setStyleSheet(f"background-color: {BADCOLOR}")
        self.volume_column.move(130, 145)
        self.volume_column.setFixedWidth(75)
        self.volume_column.setFixedHeight(30)
        self.volume_column.textChanged.connect(self.volumeColumnCheck)

        self.volume_sub_scat_l = QLabel(self)
        self.volume_sub_scat_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_sub_scat_l.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_sub_scat_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.volume_sub_scat_l.move(5, 180)
        self.volume_sub_scat_l.setFixedWidth(70)
        self.volume_sub_scat_l.setFixedHeight(30)
        self.volume_sub_scat_l.setText("Scattering")

        self.volume_sub_scat = QLineEdit(self)
        self.volume_sub_scat.setMaxLength(8)
        self.volume_sub_scat.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.volume_sub_scat.setAttribute(Qt.WA_StyledBackground, True)
        self.volume_sub_scat.setStyleSheet(f"background-color: {BADCOLOR}")
        self.volume_sub_scat.move(80, 180)
        self.volume_sub_scat.setFixedWidth(75)
        self.volume_sub_scat.setFixedHeight(30)
        self.volume_sub_scat.textChanged.connect(self.volumeSubScatCheck)

        self.albedo_ratio_l = QLabel(self)
        self.albedo_ratio_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.albedo_ratio_l.setAttribute(Qt.WA_StyledBackground, True)
        self.albedo_ratio_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.albedo_ratio_l.move(5, 215)
        self.albedo_ratio_l.setFixedWidth(50)
        self.albedo_ratio_l.setFixedHeight(30)
        self.albedo_ratio_l.setText("Ambient")

        self.albedo_ratio = QLineEdit(self)
        self.albedo_ratio.setMaxLength(8)
        self.albedo_ratio.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.albedo_ratio.setAttribute(Qt.WA_StyledBackground, True)
        self.albedo_ratio.setStyleSheet(f"background-color: {BADCOLOR}")
        self.albedo_ratio.move(5, 250)
        self.albedo_ratio.setFixedWidth(50)
        self.albedo_ratio.setFixedHeight(30)
        self.albedo_ratio.textChanged.connect(self.ratioAlbedoCheck)
        
        self.diffuse_ratio_l = QLabel(self)
        self.diffuse_ratio_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.diffuse_ratio_l.setAttribute(Qt.WA_StyledBackground, True)
        self.diffuse_ratio_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.diffuse_ratio_l.move(60, 215)
        self.diffuse_ratio_l.setFixedWidth(50)
        self.diffuse_ratio_l.setFixedHeight(30)
        self.diffuse_ratio_l.setText("Diffuse")

        self.diffuse_ratio = QLineEdit(self)
        self.diffuse_ratio.setMaxLength(8)
        self.diffuse_ratio.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.diffuse_ratio.setAttribute(Qt.WA_StyledBackground, True)
        self.diffuse_ratio.setStyleSheet(f"background-color: {BADCOLOR}")
        self.diffuse_ratio.move(60, 250)
        self.diffuse_ratio.setFixedWidth(50)
        self.diffuse_ratio.setFixedHeight(30)
        self.diffuse_ratio.textChanged.connect(self.ratioDiffuseCheck)

        self.specular_ratio_l = QLabel(self)
        self.specular_ratio_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.specular_ratio_l.setAttribute(Qt.WA_StyledBackground, True)
        self.specular_ratio_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.specular_ratio_l.move(115, 215)
        self.specular_ratio_l.setFixedWidth(50)
        self.specular_ratio_l.setFixedHeight(30)
        self.specular_ratio_l.setText("Specular")

        self.specular_ratio = QLineEdit(self)
        self.specular_ratio.setMaxLength(8)
        self.specular_ratio.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.specular_ratio.setAttribute(Qt.WA_StyledBackground, True)
        self.specular_ratio.setStyleSheet(f"background-color: {BADCOLOR}")
        self.specular_ratio.move(115, 250)
        self.specular_ratio.setFixedWidth(50)
        self.specular_ratio.setFixedHeight(30)
        self.specular_ratio.textChanged.connect(self.ratioSpecularCheck)
        
        self.shadow_ratio_l = QLabel(self)
        self.shadow_ratio_l.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.shadow_ratio_l.setAttribute(Qt.WA_StyledBackground, True)
        self.shadow_ratio_l.setStyleSheet(f"background-color: {GOODCOLOR}")
        self.shadow_ratio_l.move(170, 215)
        self.shadow_ratio_l.setFixedWidth(50)
        self.shadow_ratio_l.setFixedHeight(30)
        self.shadow_ratio_l.setText("Shadow")

        self.shadow_ratio = QLineEdit(self)
        self.shadow_ratio.setMaxLength(8)
        self.shadow_ratio.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.shadow_ratio.setAttribute(Qt.WA_StyledBackground, True)
        self.shadow_ratio.setStyleSheet(f"background-color: {BADCOLOR}")
        self.shadow_ratio.move(170, 250)
        self.shadow_ratio.setFixedWidth(50)
        self.shadow_ratio.setFixedHeight(30)
        self.shadow_ratio.textChanged.connect(self.ratioShadowCheck)

        self.shadow_ratio.setText("0.25")
        self.specular_ratio.setText("0.25")
        self.albedo_ratio.setText("0.25")
        self.diffuse_ratio.setText("0.25")
        self.light_power.setText("1.0")
        self.spec_factor.setText("3.0")
        self.spec_color.setText("0.3")
        self.volume_column.setText("0.05")
        self.volume_threshhold.setText('0.01')
        self.volume_sub_scat.setText("0.05")

    def lightPowerCheck(self):
        return self.typicalCheck(self.light_power)
    def specularColorCheck(self):
        return self.typicalCheck(self.spec_color)
    def specularFactorCheck(self):
        return self.typicalCheck(self.spec_factor)
    def volumeThreshholdCheck(self):
        return self.typicalCheck(self.volume_threshhold)
    def volumeColumnCheck(self):
        return self.typicalCheck(self.volume_column)
    def volumeSubScatCheck(self):
        return self.typicalCheck(self.volume_sub_scat)
    def ratioAlbedoCheck(self):
        return self.typicalCheck(self.albedo_ratio)
    def ratioDiffuseCheck(self):
        return self.typicalCheck(self.diffuse_ratio)
    def ratioSpecularCheck(self):
        return self.typicalCheck(self.specular_ratio)
    def ratioShadowCheck(self):
        return self.typicalCheck(self.shadow_ratio)

    def typicalCheck(self, some_element):
        number = some_element.text()
        try:
            number = float(number)
        except:
            some_element.setStyleSheet(f"background-color: {BADCOLOR}")
            self.issues = True
            return 0
        if number < 0: 
            some_element.setStyleSheet(f"background-color: {BADCOLOR}")
            self.issues = True
            return 0
        some_element.setStyleSheet(f"background-color: {GOODCOLOR}")
        return number
    
    def getSettings(self):
        self.issues = False
        light_power = self.lightPowerCheck()

        specular_color = self.specularColorCheck()
        specular_factor = self.specularFactorCheck()

        threshhold = self.volumeThreshholdCheck()
        column = self.volumeColumnCheck()
        sub_scat = self.volumeSubScatCheck()

        ratio_albedo = self.ratioAlbedoCheck()
        ratio_diffuse = self.ratioDiffuseCheck()
        ratio_specular = self.ratioSpecularCheck()
        ratio_shadow = self.ratioShadowCheck()
        print( self.issues, light_power, specular_color, specular_factor, threshhold, column, sub_scat, ratio_albedo, ratio_diffuse, ratio_specular, ratio_shadow)
        return self.issues, light_power, specular_color, specular_factor, threshhold, column, sub_scat, ratio_albedo, ratio_diffuse, ratio_specular, ratio_shadow

