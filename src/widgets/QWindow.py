from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QCloseEvent
from widgets.QMenuPanel import QMenuPanel
from widgets.QHotbar import QHotbar
from widgets.QDocumentEditor import QDocumentEditor
from QBinder import QBinder
from documents.QDocumentController import QDocumentController
from resources.QResourceProvider import QResourceProvider
from documents.QDocument import QDocument
from resources.QIcons import QIcons

class QWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))

        self.setMinimumSize(850, 420)
        self.setStyleSheet(QResourceProvider.getStyleSheet("window"))

        windowLayout = QVBoxLayout()
        windowLayout.setContentsMargins(0, 0, 0, 0)
        windowLayout.setSpacing(0)
        self.setLayout(windowLayout)

        self.binder = QBinder()

        self.documentController = QDocumentController(self.binder)

        self.panel = QMenuPanel(parent = self, binder = self.binder)
        self.layout().addWidget(self.panel)
        
        self.hotbar = QHotbar(parent = self, binder = self.binder)
        self.layout().addWidget(self.hotbar)

        self.scrollArea = QScrollArea(self)
        self.layout().addWidget(self.scrollArea)

        self.content = QWidget(self.scrollArea)
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 60, 0, 10)
        self.content.setLayout(contentLayout)

        self.scrollArea.setWidget(self.content)
        self.scrollArea.setWidgetResizable(True)

        self.editor = QDocumentEditor(parent = self.content, binder = self.binder)
        self.content.layout().addWidget(self.editor)

        self.binder.quitBinding.connect(self.close)
        self.binder.documentUpdatedBinding.connect(self.handleDocumentUpdating)
        self.editor.cursorPositionChanged.connect(self.ensureEditorCursorVisible)

        self.documentController.createBlankDocument()
    
    def ensureEditorCursorVisible(self) -> None:
        position = self.editor.mapToParent(self.editor.cursorRect().center())
        self.scrollArea.ensureVisible(position.x(), position.y())
    
    def handleDocumentUpdating(self, document: QDocument) -> None:
        self.setWindowTitle(f"Htry ~ {document.getTitle()}.htry")
        self.scrollArea.verticalScrollBar().setValue(0)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.documentController.canPerformCriticalAction():
            event.accept()
        else:
            event.ignore()