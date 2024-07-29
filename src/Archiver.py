from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject
from Binder import Binder

class Archiver(QObject):
    
    def __init__(self, parent: QWidget, binder: Binder):
        super().__init__(parent)