from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from widgets.menu_panel import QMenuPanel
from widgets.hotbar import QHotbar
from resources.icons import Icons
from resources import resource_provider
from binder import Binder

class QWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Htry")
        self.setWindowIcon(resource_provider.getIcon(Icons.LOGO))

        self.setMinimumSize(840, 420)
        self.setStyleSheet(resource_provider.getStyleSheet("window"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.binder = Binder()

        self.menu_panel = QMenuPanel(parent = self, binder = self.binder)
        self.layout().addWidget(self.menu_panel)
        
        self.hotbar = QHotbar(parent = self, binder = self.binder)
        self.layout().addWidget(self.hotbar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet(resource_provider.getStyleSheet("scroll_area"))
        self.layout().addWidget(self.scroll_area)
    
    def setup(self) -> None:
        pass