from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray, QBuffer, QIODeviceBase, QUrl
from documents.QDocument import QDocument
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib

class QDocumentArchiver:

    CONTENT_FILE_NAME = "content.html"
    COMPRESSION_TYPE = ZIP_DEFLATED
    COMPRESSION_LEVEL = 6

    @staticmethod
    def fileFormat(fileName: str) -> str:
        return fileName[fileName.rfind(".") + 1:]

    @staticmethod
    def pixmap2ByteArray(pixmap: QPixmap, format: str) -> QByteArray:
        byteArray = QByteArray()
        buffer = QBuffer(byteArray)
        buffer.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, format)
        buffer.close()

        return byteArray
    
    @staticmethod
    def byteArray2Pixmap(byteArray: QByteArray, format: str) -> QPixmap:
        pixmap = QPixmap()
        pixmap.loadFromData(byteArray, format)

        return pixmap

    @staticmethod
    def saveDocument(document: QDocument) -> None:
        content = document.toHtml()

        with ZipFile(document.filePath, mode = "w", compression = QDocumentArchiver.COMPRESSION_TYPE,
            compresslevel = QDocumentArchiver.COMPRESSION_LEVEL) as archive:
            for imageFile in document.images:
                hashcode = hashlib.sha256(imageFile.encode()).hexdigest()
                format = QDocumentArchiver.fileFormat(imageFile)
                localFile = hashcode + format
                pixmap = document.resource(QDocument.ResourceType.ImageResource, QUrl(imageFile))

                archive.writestr(localFile, QDocumentArchiver.pixmap2ByteArray(pixmap, format))
                content = content.replace(imageFile, localFile)
            
            archive.writestr(QDocumentArchiver.CONTENT_FILE_NAME, content)
    
    @staticmethod
    def readDocument(filePath: str) -> QDocument:
        document = QDocument()
        document.filePath = filePath

        with ZipFile(filePath, mode = "r") as archive:
            for resourceFile in archive.namelist():
                if resourceFile == QDocumentArchiver.CONTENT_FILE_NAME:
                    continue
                
                byteArray = QByteArray(archive.read(resourceFile))
                format = QDocumentArchiver.fileFormat(resourceFile)
                document.addResource(QDocument.ResourceType.ImageResource, 
                    QUrl(resourceFile), QDocumentArchiver.byteArray2Pixmap(byteArray, format))
            
            document.setHtml(str(archive.read(QDocumentArchiver.CONTENT_FILE), encoding = "utf-8"))
        
        return document