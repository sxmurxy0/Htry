from PyQt6.QtCore import QObject
from documents.QDocument import QDocument
from documents.QDocumentArchiver import QDocumentArchiver
from widgets.QDialogService import QDialogService
from QBinder import QBinder

class QDocumentController(QObject):

    def __init__(self, binder: QBinder) -> None:
        super().__init__()

        self.filePath = None
        self.document = None
        self.binder = binder

        self.binder.createDocumentBinding.connect(self.createBlankDocument)
        self.binder.openDocumentBinding.connect(self.openDocument)
        self.binder.saveDocumentBinding.connect(self.saveDocument)
        self.binder.saveDocumentAsBinding.connect(self.saveDocumentAs)
    
    def setDocument(self, filePath: str, document: QDocument) -> None:
        self.filePath = filePath
        self.document = document

        self.binder.documentUpdatedBinding.emit(self.document)
    
    def canPerformCriticalAction(self) -> bool:
        if not self.document or not self.document.isModified():
            return True
        
        response = QDialogService.getCriticalSavingResponse()
        if response == QDialogService.Response.ACCEPT:
            self.saveDocument()
        
        return response != QDialogService.Response.CANCEL
    
    def createBlankDocument(self) -> None:
        if self.canPerformCriticalAction():
            self.setDocument(filePath = None, document = QDocument())

    def saveDocument(self) -> None:
        if self.filePath:
            QDocumentArchiver.saveDocument(self.filePath, self.document)
            self.document.setModified(False)
        else:
            self.saveDocumentAs()
    
    def saveDocumentAs(self) -> None:
        filePath = QDialogService.getSaveDocumentAsFile(self.document.getTitle())
        if filePath:
            self.filePath = filePath
            self.saveDocument()

    def openDocument(self) -> None:
        filePath = QDialogService.getOpenDocumentFile()
        if filePath and self.canPerformCriticalAction():
            self.setDocument(filePath = filePath, 
                document = QDocumentArchiver.readDocument(filePath))