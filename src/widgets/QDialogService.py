from PyQt6.QtWidgets import QDialog, QFileDialog, QFrame, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QColor, QIcon
from resources.QIcons import QIcons
from resources.QResourceProvider import QResourceProvider
from enum import IntEnum
import typing

class QDialogService:

    HTRY_FILE_FILTER = "Htry-Архив (*.htry)"
    IMAGE_FILE_FILTER = "Изображение (*.png; *.jpg; *.jpeg; *.gif; *.bmp)"

    class Response(IntEnum):
        CANCEL = 0
        ACCEPT = 1
        REJECT = 2

    class QCriticalSavingDialog(QDialog):

        def __init__(self):
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Предупреждение")

            self.setFixedSize(305, 110)
            self.setStyleSheet(QResourceProvider.getStyleSheet("dialog"))
            
            self.iconLabel = QLabel(self)
            self.iconLabel.setPixmap(QResourceProvider.getIcon(QIcons.CRITICAL)
                .pixmap(40, 40, mode = QIcon.Mode.Normal))
            self.iconLabel.setScaledContents(True)
            self.iconLabel.setGeometry(14, 13, 40, 40)
            
            self.titleLabel = QLabel(parent = self,
                text = "Документ содержит несохраненные\nизменения. Сохранить его?")
            self.titleLabel.setObjectName("title")
            self.titleLabel.setGeometry(66, 13, 240, 40)

            self.decoration = QFrame(self)
            self.decoration.setObjectName("decoration")
            self.decoration.setGeometry(0, 66, 305, 44)

            self.acceptButton = QPushButton(parent = self, text = "Да")
            self.acceptButton.setProperty("modal_button", True)
            self.acceptButton.setGeometry(68, 76, 61, 24)
            self.acceptButton.clicked.connect(
                lambda: self.done(QDialogService.Response.ACCEPT.value))
            
            self.rejectButton = QPushButton(parent = self, text = "Нет")
            self.rejectButton.setProperty("modal_button", True)
            self.rejectButton.setGeometry(138, 76, 61, 24)
            self.rejectButton.clicked.connect(
                lambda: self.done(QDialogService.Response.REJECT.value))

            self.cancelButton = QPushButton(parent = self, text = "Отмена")
            self.cancelButton.setProperty("modal_button", True)
            self.cancelButton.setGeometry(208, 76, 81, 24)
            self.cancelButton.clicked.connect(
                lambda: self.done(QDialogService.Response.CANCEL.value))
    
    class QColorPickerDialog(QDialog):
        def __init__(self) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Выберите цвет")
    
    class QLinkInsertionDialog(QDialog):

        def __init__(self, text: str) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Вставка ссылки")

            self.setFixedSize(336, 139)
            self.setStyleSheet(QResourceProvider.getStyleSheet("dialog"))

            self.textInput = QLineEdit(self)
            self.textInput.setPlaceholderText("Заголовок")
            self.textInput.setGeometry(18, 14, 300, 28)

            self.urlInput = QLineEdit(self)
            self.urlInput.setPlaceholderText("URL")
            self.urlInput.setGeometry(18, 50, 300, 28)

            self.decoration = QFrame(self)
            self.decoration.setObjectName("decoration")
            self.decoration.setGeometry(0, 94, 336, 45)

            self.acceptButton = QPushButton(parent = self, text = "Вставить")
            self.acceptButton.setProperty("modal_button", True)
            self.acceptButton.setGeometry(146, 104, 81, 24)
            self.acceptButton.clicked.connect(
                lambda: self.done(QDialogService.Response.ACCEPT.value))

            self.cancelButton = QPushButton(parent = self, text = "Отмена")
            self.cancelButton.setProperty("modal_button", True)
            self.cancelButton.setGeometry(236, 104, 81, 24)
            self.cancelButton.clicked.connect(
                lambda: self.done(QDialogService.Response.CANCEL.value))
            
            self.textInput.setText(text)
        
        def getResult(self) -> typing.Tuple[str, str]:
            return (self.textInput.text(), self.urlInput.text())

    @staticmethod
    def getCriticalSavingResponse() -> int:
        code = QDialogService.QCriticalSavingDialog().exec()
        return QDialogService.Response(code)

    @staticmethod
    def getOpenDocumentFile() -> str:
        return QFileDialog.getOpenFileName(caption = "Открыть",
            filter = QDialogService.HTRY_FILE_FILTER)[0]

    @staticmethod
    def getSaveDocumentAsFile(fileName: str = None) -> str:
        return QFileDialog.getSaveFileName(directory = fileName, 
            caption = "Сохранить как", filter = QDialogService.HTRY_FILE_FILTER)[0]
    
    @staticmethod
    def getImageInsertionFile() -> str:
        return QFileDialog.getOpenFileName(caption = "Вставка изображения",
            filter = QDialogService.IMAGE_FILE_FILTER)[0]
    
    @staticmethod
    def getLinkInsertionData(text: str = None) -> typing.Tuple[str, str]:
        dialog = QDialogService.QLinkInsertionDialog(text)
        code = dialog.exec()

        if code == QDialogService.Response.ACCEPT:
            return dialog.getResult()
        
        return None
    
    @staticmethod
    def getColor(color: QColor = None) -> QColor:
        return QDialogService.QColorPickerDialog().exec()