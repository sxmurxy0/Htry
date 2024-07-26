from PyQt6.QtWidgets import QWidget, QFrame, QMenu, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

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