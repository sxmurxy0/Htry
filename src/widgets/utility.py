from PyQt6.QtWidgets import QWidget, QFrame, QMenu, QSpacerItem, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QSize

class QVerticalSeparator(QFrame):
    
    def __init__(self, parent: QWidget, height: int) -> None:
        super().__init__(parent)
        self.setFixedSize(1, height)

def addVerticalSeparator(widget: QWidget, height: int) -> None:
    separator = QVerticalSeparator(parent = widget, height = height)
    widget.layout().addWidget(separator)

def addHorizontalSpacer(widget: QWidget) -> None:
    spacer = QSpacerItem(0, 0,
        hPolicy = QSizePolicy.Policy.Expanding, vPolicy = QSizePolicy.Policy.Minimum)
    widget.layout().addItem(spacer)

def setMenuAttributes(menu: QMenu) -> None:
    menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint 
        | Qt.WindowType.NoDropShadowWindowHint)

def setButtonParameters(button: QPushButton, width, height, icon_width, icon_height, checkable = False) -> None:
    button.setFixedSize(width, height)
    button.setIconSize(QSize(icon_width, icon_height))
    button.setCheckable(checkable)