from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QPushButton, QDialog, QFileDialog
from core.resources.Icons import Icons
from core.resources import QResourceProvider
from enum import Enum

class QCriticalSavingDialog(QDialog):

    class Response(Enum):
        ACCEPT = 1
        REJECT = 2
        CANCEL = 3

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setWindowTitle("Предупреждение")

        self.setFixedSize(305, 110)
        self.setStyleSheet(QResourceProvider.getStyleSheet("critical_dialog"))

        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(QResourceProvider.getIcon(Icons.CRITICAL).pixmap(40, 40))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setGeometry(14, 13, 40, 40)
        
        self.titleLabel = QLabel(parent = self,
            text = "Документ содержит несохраненные\nизменения. Сохранить его?")
        self.titleLabel.setGeometry(66, 13, 261, 40)

        self.decoration = QFrame(self)
        self.decoration.setObjectName("decoration")
        self.decoration.setGeometry(0, 66, 312, 44)

        self.acceptButton = QPushButton(parent = self, text = "Да")
        self.acceptButton.setGeometry(68, 76, 61, 24)
        self.acceptButton.clicked.connect(
            lambda: self.done(QCriticalSavingDialog.Response.ACCEPT.value))

        self.rejectButton = QPushButton(parent = self, text = "Нет")
        self.rejectButton.setGeometry(138, 76, 61, 24)
        self.rejectButton.clicked.connect(
            lambda: self.done(QCriticalSavingDialog.Response.REJECT.value))

        self.cancelButton = QPushButton(parent = self, text = "Отмена")
        self.cancelButton.setGeometry(208, 76, 81, 24)
        self.cancelButton.clicked.connect(
            lambda: self.done(QCriticalSavingDialog.Response.CANCEL.value))

def getCriticalSavingResponse(parent: QWidget) -> QCriticalSavingDialog.Response:
    code = QCriticalSavingDialog(parent).exec()
    for response in QCriticalSavingDialog.Response:
        if response.value == code:
            return response
    
    return response.CANCEL

FILE_FILTER = "Htry-Архив (*.htry)"

def getOpenDocumentFile(parent: QWidget) -> str:
    return QFileDialog.getOpenFileName(parent = parent, caption = "Открыть",
        filter = FILE_FILTER)[0]

def getSaveAsDocumentFile(parent: QWidget, fileName: str = None) -> str:
    return QFileDialog.getSaveFileName(parent = parent, directory = fileName, 
        caption = "Сохранить как", filter = FILE_FILTER)[0]