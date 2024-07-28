from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollBar, QScrollArea
from PyQt6.QtCore import Qt
from widgets.menu_panel import QMenuPanel
from widgets.hotbar import QHotbar
from widgets.document_editor import QDocumentEditor
from widgets import utility
from resources.icons import Icons
from resources import resource_provider
from binder import Binder

class QWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Htry")
        self.setWindowIcon(resource_provider.getIcon(Icons.LOGO))

        self.setMinimumSize(850, 420)
        self.setStyleSheet(resource_provider.getStyleSheet("window"))

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        self.setLayout(window_layout)
        
        self.binder = Binder()

        self.menu_panel = QMenuPanel(parent = self, binder = self.binder)
        self.layout().addWidget(self.menu_panel)
        
        self.hotbar = QHotbar(parent = self, binder = self.binder)
        self.layout().addWidget(self.hotbar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet(resource_provider.getStyleSheet("scroll_area"))
        self.layout().addWidget(self.scroll_area)

        self.content = QWidget()

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 60, 0, 10)
        self.content.setLayout(content_layout)
        
        self.editor = QDocumentEditor(parent = self.content,
            scroll_area = self.scroll_area, binder = self.binder)
        self.content.layout().addWidget(self.editor)

        self.scroll_area.setWidget(self.content)
        self.scroll_area.setWidgetResizable(True)
    
    def setup(self) -> None:
        pass