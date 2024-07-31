from PyQt6.QtCore import QObject, QFile
from documents.QDocument import QDocument
from documents.QDocumentArchiver import QDocumentArchiver
from widgets.QDialogService import QDialogService
from QBinder import QBinder

class QDocumentController(QObject):

    def __init__(self, binder: QBinder) -> None:
        super().__init__()

        self.document = None
        self.updateBinding = binder.documentUpdatedBinding

        binder.createDocumentBinding.connect(self.createBlankDocument)
        binder.openDocumentBinding.connect(self.openDocument)
        binder.saveDocumentBinding.connect(self.saveDocument)
        binder.saveDocumentAsBinding.connect(self.saveDocumentAs)
    
    def ensureCriticalAction(self) -> bool:
        if not self.document or not self.document.hasUnsavedChanges:
            return True
        
        response = QDialogService.getCriticalSavingResponse()
        if response == QDialogService.Response.ACCEPT:
            self.saveDocument()
        
        return response != QDialogService.Response.CANCEL
    
    def setDocument(self, document: QDocument) -> None:
        self.document = document
        self.updateBinding.emit(self.document)
    
    def createBlankDocument(self) -> None:
        if self.ensureCriticalAction():
            self.setDocument(QDocument())

    def saveDocument(self) -> None:
        if self.document.filePath:
            QDocumentArchiver.saveDocument(self.document)
            self.document.handleSaving()
        else:
            self.saveDocumentAs()
    
    def saveDocumentAs(self) -> None:
        filePath = QDialogService.getSaveDocumentAsFile(self.document.fileName())
        if filePath:
            self.document.filePath = filePath
            self.saveDocument()

    def openDocument(self) -> None:
        filePath = QDialogService.getOpenDocumentFile()
        if QFile.exists(filePath) and self.ensureCriticalAction():
            self.setDocument(QDocumentArchiver.readDocument(filePath))