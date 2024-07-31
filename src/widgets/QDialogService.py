from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QPushButton, QDialog, QFileDialog
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QIODeviceBase
from resources.Icons import Icons
from resources.QResourceProvider import QResourceProvider
from enum import Enum

class QDialogService:

    HTRY_FILE_FILTER = "Htry-Архив (*.htry)"

    class Response(Enum):
        ACCEPT = 1
        REJECT = 2
        CANCEL = 3

    class QCriticalSavingDialog(QDialog):

        def __init__(self):
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(Icons.LOGO))
            self.setWindowTitle("Предупреждение")

            self.setFixedSize(305, 110)
            self.setStyleSheet(QResourceProvider.getStyleSheet("dialog"))
            
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
                lambda: self.done(QDialogService.Response.ACCEPT.value))
            
            self.rejectButton = QPushButton(parent = self, text = "Нет")
            self.rejectButton.setGeometry(138, 76, 61, 24)
            self.rejectButton.clicked.connect(
                lambda: self.done(QDialogService.Response.REJECT.value))

            self.cancelButton = QPushButton(parent = self, text = "Отмена")
            self.cancelButton.setGeometry(208, 76, 81, 24)
            self.cancelButton.clicked.connect(
                lambda: self.done(QDialogService.Response.CANCEL.value))
    
    class QColorPickerDialog(QDialog):

        def __init__(self) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(Icons.LOGO))
            self.setWindowTitle("Выберите цвет")

    @staticmethod
    def getCriticalSavingResponse() -> Response:
        code = QDialogService.QCriticalSavingDialog().exec()
        for response in QDialogService.Response:
            if response.value == code:
                return response
        
        return QDialogService.Response.CANCEL

    @staticmethod
    def getOpenDocumentFile() -> str:
        return QFileDialog.getOpenFileName(caption = "Открыть",
            filter = QDialogService.HTRY_FILE_FILTER)[0]

    @staticmethod
    def getSaveDocumentAsFile(fileName: str) -> str:
        return QFileDialog.getSaveFileName(directory = fileName, 
            caption = "Сохранить как", filter = QDialogService.HTRY_FILE_FILTER)[0]
    
    @staticmethod
    def getColor(color: QColor = None) -> QColor:
        return QDialogService.QColorPickerDialog().exec()