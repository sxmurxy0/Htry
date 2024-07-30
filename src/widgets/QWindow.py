from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QCloseEvent
from widgets.QDialogService import QCriticalSavingDialog
from widgets.QMenuPanel import QMenuPanel
from widgets.QHotbar import QHotbar
from widgets.QDocumentEditor import QDocumentEditor
from core.QBinder import QBinder
from core.documents.QDocument import QDocument
from core.resources.Icons import Icons
from core.resources import QResourceProvider
from widgets import QDialogService
from core.documents import QDocumentArhiver

class QWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowIcon(QResourceProvider.getIcon(Icons.LOGO))

        self.setMinimumSize(850, 420)
        self.setStyleSheet(QResourceProvider.getStyleSheet("window"))

        windowLayout = QVBoxLayout()
        windowLayout.setContentsMargins(0, 0, 0, 0)
        windowLayout.setSpacing(0)
        self.setLayout(windowLayout)

        self.binder = QBinder()
        self.document = None

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

        self.binder.createDocumentBinding.connect(self.createBlankDocument)
        self.binder.openDocumentBinding.connect(self.openDocument)
        self.binder.saveDocumentBinding.connect(self.saveDocument)
        self.binder.saveDocumentAsBinding.connect(self.saveDocumentAs)
        self.binder.quitBinding.connect(self.close)

        self.editor.cursorPositionChanged.connect(self.ensureEditorCursorVisible)

        self.createBlankDocument()
    
    def ensureEditorCursorVisible(self) -> None:
        position = self.editor.mapToParent(self.editor.cursorRect().center())
        self.scrollArea.ensureVisible(position.x(), position.y())
    
    def ensureCriticalAction(self) -> bool:
        if not self.document or not self.document.hasUnsavedChanges:
            return True
        
        response = QDialogService.getCriticalSavingResponse(self)
        if response == QCriticalSavingDialog.Response.ACCEPT:
            self.saveDocument()
        
        return response != QCriticalSavingDialog.Response.CANCEL
    
    def createBlankDocument(self) -> None:
        if self.ensureCriticalAction():
            self.setDocument(QDocument())
    
    def openDocument(self) -> None:
        filePath = QDialogService.getOpenDocumentFile(self)

        if filePath and self.ensureCriticalAction():
            self.setDocument(QDocumentArhiver.openDocument(filePath))
    
    def setDocument(self, document: QDocument) -> None:
        self.document = document
        self.editor.setDocument(self.document)
      
        self.setWindowTitle(f"Htry ~ {self.document.getFileName()}.htry")

    def saveDocument(self) -> None:
        if self.document.filePath:
            QDocumentArhiver.saveDocument(self.document)
            self.document.hasUnsavedChanges = False
        else:
            self.saveDocumentAs()

    def saveDocumentAs(self) -> None:
        filePath = QDialogService.getSaveAsDocumentFile(parent = self, 
            fileName = self.document.getFileName())
        
        if filePath:
            self.document.filePath = filePath
            self.saveDocument()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.ensureCriticalAction():
            event.accept()
        else:
            event.ignore()