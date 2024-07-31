from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import QFile
import typing

class QDocument(QTextDocument):

    UNDEFINED_FILE_NAME = "Untitled.htry"

    def __init__(self) -> None:
        super().__init__()
        
        self.filePath = None
        self.images = []
        self.hasUnsavedChanges = False
        
        self.contentsChanged.connect(self.handleContentChanging)
    
    def handleContentChanging(self) -> None:
        self.hasUnsavedChanges = True
    
    def handleSaving(self) -> None:
        self.hasUnsavedChanges =False
    
    def fileName(self) -> str:
        if self.filePath:
            i = self.filePath.rfind("/")
            return self.filePath[i + 1:]
        
        return QDocument.UNDEFINED_FILE_NAME
    
    def addResource(self, type: int, file: QFile, resource: typing.Any) -> None:
        super().addResource(type, file, resource)
        if type == QTextDocument.ResourceType.ImageResource:
            self.__images.append(file.toString())