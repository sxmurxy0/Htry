from PyQt6.QtWidgets import QWidget, QVBoxLayout
from widgets.MenuPanel import *
from widgets.Hotbar import *
from widgets.DocumentEditor import *
from resources.Icons import *
from resources import ResourceProvider
from Archiver import *
from Binder import *

class QWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Htry")
        self.setWindowIcon(ResourceProvider.getIcon(Icons.LOGO))

        self.setMinimumSize(850, 420)
        self.setStyleSheet(ResourceProvider.loadStyleSheet("window"))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        self.binder = Binder(parent = self)

        self.archiver = Archiver(parent = self, binder = self.binder)

        self.panel = QMenuPanel(parent = self, binder = self.binder)
        self.layout().addWidget(self.panel)
        
        self.hotbar = QHotbar(parent = self, binder = self.binder)
        self.layout().addWidget(self.hotbar)

        self.editor = QDocumentEditor(parent = self, binder = self.binder)
        self.layout().addWidget(self.editor)