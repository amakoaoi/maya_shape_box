import os

from maya import cmds
from maya_helper import MayaDockableWindow, MayaWindow
from PySide2 import QtWidgets as QW
from PySide2 import QtGui as UI
from PySide2 import QtCore as QC
from functools import partial
from shape_box_functions import change_color, change_shape


class ShapeBox(MayaDockableWindow):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("Maya Shape Box")

        main_layout = QW.QVBoxLayout()
        shape_button_layout = QW.QGridLayout()
        color_button_layout = QW.QHBoxLayout()
        custom_color_layout = QW.QHBoxLayout()

        self.setLayout(main_layout)

        font = UI.QFont()
        font.setBold(True)

        shape_label = QW.QLabel("SHAPES")
        shape_label.setStyleSheet("background-color: #772ba3; border: 1px solid #5a197f")
        shape_label.setMinimumSize(300, 25)
        shape_label.setMaximumHeight(25)
        shape_label.setAlignment(QC.Qt.AlignCenter)
        shape_label.setFont(font)
        color_label = QW.QLabel("COLORS")
        color_label.setStyleSheet("background-color: #772ba3; border: 1px solid #5a197f")
        color_label.setMinimumSize(300, 25)
        color_label.setMaximumHeight(25)
        color_label.setAlignment(QC.Qt.AlignCenter)
        color_label.setFont(font)
        custom_color_button = QW.QPushButton("Custom color")
        custom_color_button.setMinimumHeight(35)

        self.custom_color = None
        self.saved_custom_color = QW.QPushButton()
        if cmds.optionVar(exists='custom_color'):
            self.custom_color = cmds.optionVar(query='custom_color')
            self.saved_custom_color.setStyleSheet("background-color: {}".format(self.custom_color))
        else:
            self.saved_custom_color.setEnabled(False)
        self.saved_custom_color.clicked.connect(lambda: self.change_color(self.custom_color))
        self.saved_custom_color.setFixedSize(35, 35)

        custom_color_layout.addWidget(custom_color_button)
        custom_color_layout.addWidget(self.saved_custom_color)

        main_layout.addWidget(shape_label)
        main_layout.addLayout(shape_button_layout)
        main_layout.addWidget(color_label)
        main_layout.addLayout(color_button_layout)
        main_layout.addLayout(custom_color_layout)

        buttons_name = ["circle", "square", "locator", "crossed_arrow", "arrow",
                        "cube", "diamond", "double_arrow", "double_curved_arrow", "triangle"]

        color_name = {"red": "ff0400", "green": "18ff00", "blue": "0000ff", "yellow": "fff600", "cyan": "00fff6", "pink": "f000ff", "purple": "7800ff", "white": "ffffff"}

        self.color_picker = QW.QColorDialog()
        self.color_picker.colorSelected.connect(self.chosen_color)
        custom_color_button.clicked.connect(lambda: self.color_picker.show())

        for i, name in enumerate(buttons_name):
            button = QW.QPushButton()
            button.setFixedSize(60, 60)

            pixmap = UI.QPixmap(os.path.join(os.path.dirname(__file__), "icons/{}_icon.png".format(name)))
            mask = pixmap.createMaskFromColor(UI.QColor('black'), QC.Qt.MaskOutColor)
            pixmap.fill(UI.QColor('#ffffff'))
            pixmap.setMask(mask)
            button.setIcon(UI.QIcon(pixmap))
            button.setIconSize(QC.QSize(55, 55))

            button.setToolTip(name)
            button.setStatusTip(name)
            button.setWhatsThis(name)
            if i < 5:
                shape_button_layout.addWidget(button, 0, i)
            else:
                shape_button_layout.addWidget(button, 1, i-5)
            button.clicked.connect(partial(self.change_shapes, name))

        for name in color_name:
            button = QW.QPushButton()
            button.setFixedSize(35, 35)
            button.setStyleSheet("background-color: #{}".format(color_name[name]))
            button.setToolTip(name)
            button.setStatusTip(name)
            button.setWhatsThis(name)
            color_button_layout.addWidget(button)
            button.clicked.connect(partial(self.change_color, "#" + color_name[name]))

        self.show()

    @staticmethod
    def change_shapes(name):
        change_shape(name)

    @staticmethod
    def change_color(hex_color):
        change_color(hex_color)

    def chosen_color(self, color):
        self.custom_color = color.name()
        self.saved_custom_color.setEnabled(True)
        self.saved_custom_color.setStyleSheet("background-color: {}".format(color.name()))
        cmds.optionVar(stringValue=('custom_color', self.custom_color))
