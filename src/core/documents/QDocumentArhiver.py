from PyQt6.QtGui import QTextImageFormat, QTextCursor
from core.documents.QDocument import QDocument
from zipfile import ZipFile
    
def saveDocument(document: QDocument) -> None:
    pass

    # images = []
    # block = self.document.begin()
    
    # while (block.isValid()):
    #     it = block.begin()
    #     while not it.atEnd():
    #         fragment = it.fragment()
    #         if (fragment.isValid() and fragment.charFormat().isImageFormat()):
    #             images.append(fragment.charFormat().toImageFormat().name())
    #         it += 1
    #     block = block.next()
    
    # with ZipFile(self.filePath, "w") as _zip:
    #     for image in images:
    #         _zip.write(image)
    #     _zip.writestr("content.html", self.document.toHtml())

def openDocument(filePath: str) -> QDocument:
    return None

    # with open(filePath, "r") as file:
    #     s = file.read()
    #     print(s)
    #     self.document = QTextDocument()
    #     self.document.setHtml(s)
    # self.binder.documentCreatedBinding.emit(self.document)