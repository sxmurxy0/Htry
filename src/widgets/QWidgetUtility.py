from PyQt6.QtWidgets import QWidget, QFrame, QMenu, QSpacerItem, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QSize

class QWidgetUtility:

    class QVerticalSeparator(QFrame):
        
        def __init__(self, parent: QWidget, height: int) -> None:
            super().__init__(parent)
            self.setFixedSize(1, height)

    @staticmethod
    def addVerticalSeparator(widget: QWidget, height: int) -> None:
        separator = QWidgetUtility.QVerticalSeparator(parent = widget, height = height)
        widget.layout().addWidget(separator)

    @staticmethod
    def addHorizontalSpacer(widget: QWidget) -> None:
        spacer = QSpacerItem(0, 0,
            hPolicy = QSizePolicy.Policy.Expanding, vPolicy = QSizePolicy.Policy.Minimum)
        widget.layout().addItem(spacer)

    @staticmethod
    def addVerticalSpacer(widget: QWidget) -> None:
        spacer = QSpacerItem(0, 0,
            hPolicy = QSizePolicy.Policy.Minimum, vPolicy = QSizePolicy.Policy.Expanding)
        widget.layout().addItem(spacer)

    @staticmethod
    def setMenuAttributes(menu: QMenu) -> None:
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint 
            | Qt.WindowType.NoDropShadowWindowHint)

    @staticmethod
    def setButtonParameters(button: QPushButton, width: int, height: int,
            iconWidth: int, iconHeight: int, checkable: bool = False) -> None:
        button.setFixedSize(width, height)
        button.setIconSize(QSize(iconWidth, iconHeight))
        button.setCheckable(checkable)