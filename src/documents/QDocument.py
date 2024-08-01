from PyQt6.QtGui import QTextDocument
from PyQt6.QtCore import QUrl
import typing

class QDocument(QTextDocument):

    def __init__(self, title: str = "Untitled") -> None:
        super().__init__()
        
        self.title = title
        self.images = []
    
    def getTitle(self) -> str:
        return self.title
    
    def getImages(self) -> typing.Iterable[str]:
        return self.images
    
    def addResource(self, type: int, url: QUrl, resource: typing.Any) -> None:
        super().addResource(type, url, resource)
        if type == QTextDocument.ResourceType.ImageResource:
            self.images.append(url.toString())