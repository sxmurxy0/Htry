from PyQt6.QtGui import QTextDocument

class QDocument(QTextDocument):

    def __init__(self, filePath: str = None) -> None:
        super().__init__()
        
        self.filePath = filePath
        self.hasUnsavedChanges = False

        self.contentsChanged.connect(self.handleContentChange)
    
    def handleContentChange(self) -> None:
        self.hasUnsavedChanges = True
    
    def getFileName(self) -> str:
        if self.filePath:
            i = self.filePath.rfind("/")
            name = self.filePath[i + 1:]
        else:
            return "Untitled"