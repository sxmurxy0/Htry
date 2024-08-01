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
    def getFileName(filePath: str) -> str:
        i, j = filePath.rfind("/") + 1, filePath.rfind(".")
        return filePath[i:j]

    @staticmethod
    def getFileFormat(fileName: str) -> str:
        i = fileName.rfind(".") + 1
        return fileName[i:]

    @staticmethod
    def pixmap2ByteArray(pixmap: QPixmap, format: str) -> QByteArray:
        byteArray = QByteArray()
        buffer = QBuffer(byteArray)
        buffer.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        pixmap.save(device = buffer, format = format)
        buffer.close()

        return byteArray
    
    @staticmethod
    def byteArray2Pixmap(byteArray: QByteArray, format: str) -> QPixmap:
        pixmap = QPixmap()
        pixmap.loadFromData(buf = byteArray, format = format)

        return pixmap

    @staticmethod
    def saveDocument(filePath: str, document: QDocument) -> None:
        content = document.toHtml()
        
        with ZipFile(filePath, mode = "w", compression = QDocumentArchiver.COMPRESSION_TYPE,
                compresslevel = QDocumentArchiver.COMPRESSION_LEVEL) as archive:
            for imageFile in document.getImages():
                hash = hashlib.sha256(imageFile.encode()).hexdigest()
                format = QDocumentArchiver.getFileFormat(imageFile)

                pixmap = document.resource(QDocument.ResourceType.ImageResource, QUrl(imageFile))
                byteArray = QDocumentArchiver.pixmap2ByteArray(pixmap, format)
                archiveFile = hash + "." + format

                archive.writestr(archiveFile, byteArray)
                content = content.replace(imageFile, archiveFile)
            
            archive.writestr(QDocumentArchiver.CONTENT_FILE_NAME, content)
    
    @staticmethod
    def readDocument(filePath: str) -> QDocument:
        document = QDocument(QDocumentArchiver.getFileName(filePath))

        with ZipFile(filePath, mode = "r") as archive:
            for archiveFile in archive.namelist():
                if archiveFile == QDocumentArchiver.CONTENT_FILE_NAME:
                    continue
                
                format = QDocumentArchiver.getFileFormat(archiveFile)
                byteArray = QByteArray(archive.read(archiveFile))
                pixmap = QDocumentArchiver.byteArray2Pixmap(byteArray, format)

                document.addResource(QDocument.ResourceType.ImageResource,
                    QUrl(archiveFile), pixmap)
            
            content = str(archive.read(QDocumentArchiver.CONTENT_FILE_NAME), encoding = "utf-8")
            document.setHtml(content)
        
        return document