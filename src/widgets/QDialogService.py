from PyQt6.QtWidgets import (QDialog, QFileDialog, QFrame, QLabel, QPushButton,
    QLineEdit, QSpinBox, QColorDialog, QListWidget)
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt, QSize
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
            self.setStyleSheet(QResourceProvider.getStyleSheet("saving_dialog"))
            
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
    
    class QLinkInsertionDialog(QDialog):

        def __init__(self, text: str) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Вставка ссылки")

            self.setFixedSize(336, 139)

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
    
    class QImageSizeDialog(QDialog):

        def __init__(self, maxWidth: int, maxHeight: int) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Размер изображения")

            self.setFixedSize(257, 106)

            self.label = QLabel(self, text = "x")
            self.label.setGeometry(26, 16, 205, 28)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.widthSpinBox = QSpinBox(self)
            self.widthSpinBox.setGeometry(26, 16, 91, 28)
            self.widthSpinBox.setRange(0, maxWidth)

            self.heightSpinBox = QSpinBox(self)
            self.heightSpinBox.setGeometry(140, 16, 91, 28)
            self.heightSpinBox.setRange(0, maxHeight)

            self.decoration = QFrame(self)
            self.decoration.setObjectName("decoration")
            self.decoration.setGeometry(0, 60, 257, 46)

            self.acceptButton = QPushButton(parent = self, text = "Применить")
            self.acceptButton.setProperty("modal_button", True)
            self.acceptButton.setGeometry(130, 70, 101, 24)
            self.acceptButton.clicked.connect(
                lambda: self.done(QDialogService.Response.ACCEPT.value))
        
        def getResult(self) -> QSize:
            return QSize(self.widthSpinBox.value(), self.heightSpinBox.value())
    
    class QIntegerInputDialog(QDialog):

        def __init__(self, value: int) -> None:
            super().__init__()

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Ввод значения")

            self.setFixedSize(243, 105)

            self.inputSpinBox = QSpinBox(self)
            self.inputSpinBox.setGeometry(26, 16, 190, 28)
            self.inputSpinBox.setRange(0, 1000)

            self.decoration = QFrame(self)
            self.decoration.setObjectName("decoration")
            self.decoration.setGeometry(0, 60, 243, 45)

            self.acceptButton = QPushButton(parent = self, text = "Применить")
            self.acceptButton.setProperty("modal_button", True)
            self.acceptButton.setGeometry(26, 70, 101, 24)
            self.acceptButton.clicked.connect(
                lambda: self.done(QDialogService.Response.ACCEPT.value))
            
            self.cancelButton = QPushButton(parent = self, text = "Отмена")
            self.cancelButton.setProperty("modal_button", True)
            self.cancelButton.setGeometry(136, 70, 81, 24)
            self.cancelButton.clicked.connect(
                lambda: self.done(QDialogService.Response.CANCEL.value))
            
            self.inputSpinBox.setValue(value)
        
        def getResult(self) -> int:
            return self.inputSpinBox.value()
    
    class QStyleEditorDialog(QDialog):

        def __init__(self, style: dict) -> None:
            super().__init__()

            self.style = style

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Редактор стиля")
        
    class QStyleListDialog(QDialog):

        def __init__(self, data: dict, style: str) -> None:
            super().__init__()

            self.data = data

            self.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
            self.setWindowTitle("Стили")

            self.setFixedSize(346, 269)
            self.setStyleSheet(QResourceProvider.getStyleSheet("style_list_dialog"))

            self.listWidget = QListWidget(self)
            self.listWidget.setGeometry(64, 20, 256, 192)

            i = 0
            for key in data.keys():
                self.listWidget.addItem(key)
                if key == style:
                    self.listWidget.setCurrentRow(i)
                i += 1

            self.addButton = QPushButton(parent = self,
                icon = QResourceProvider.getIcon(QIcons.PLUS))
            self.addButton.setProperty("control_button", True)
            self.addButton.setGeometry(26, 20, 28, 28)
            self.addButton.clicked.connect(self.createStyle)

            self.editButton = QPushButton(parent = self,
                icon = QResourceProvider.getIcon(QIcons.PENCIL))
            self.editButton.setProperty("control_button", True)
            self.editButton.setGeometry(26, 60, 28, 28)
            self.editButton.clicked.connect(self.editStyle)
            
            self.removeButton = QPushButton(parent = self,
                icon = QResourceProvider.getIcon(QIcons.REMOVE))
            self.removeButton.setProperty("control_button", True)
            self.removeButton.setGeometry(26, 100, 28, 28)
            self.removeButton.clicked.connect(self.removeStyle)

            self.decoration = QFrame(self)
            self.decoration.setObjectName("decoration")
            self.decoration.setGeometry(0, 224, 346, 45)

            self.acceptButton = QPushButton(parent = self, text = "Применить")
            self.acceptButton.setProperty("modal_button", True)
            self.acceptButton.setGeometry(230, 235, 91, 24)
            self.acceptButton.clicked.connect(
                lambda: self.done(QDialogService.Response.ACCEPT.value))
            
        def createStyle(self) -> None:
            pass
        
        def editStyle(self) -> None:
            pass
        
        def removeStyle(self) -> None:
            item = self.listWidget.item(self.listWidget.currentRow())
            if item:
                self.data.pop(item.text())
                self.listWidget.takeItem(self.listWidget.row(item))
    
        def getResult(self) -> str:
            item = self.listWidget.item(self.listWidget.currentRow())
            if item:
                return item.text()
            else:
                return ''

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
    def getColor(color: QColor = None) -> QColor:
        dialog = QColorDialog(color)
        dialog.setWindowIcon(QResourceProvider.getIcon(QIcons.LOGO))
        dialog.setWindowTitle("Выбор цвета")
        dialog.setStyleSheet(QResourceProvider.getStyleSheet("color_dialog"))
        code = dialog.exec()
    
        return None if code == QDialogService.Response.CANCEL else dialog.currentColor()
    
    @staticmethod
    def getImageInsertionFile() -> str:
        return QFileDialog.getOpenFileName(caption = "Вставка изображения",
            filter = QDialogService.IMAGE_FILE_FILTER)[0]
    
    @staticmethod
    def getImageSize(maxWidth: int = 2560, maxHeight: int = 1920) -> QSize:
        dialog = QDialogService.QImageSizeDialog(maxWidth = maxWidth, maxHeight = maxHeight)
        dialog.exec()
        return dialog.getResult()
    
    @staticmethod
    def getLinkInsertionData(text: str = None) -> typing.Tuple[str, str]:
        dialog = QDialogService.QLinkInsertionDialog(text)
        code = dialog.exec()
        return None if code != QDialogService.Response.ACCEPT else dialog.getResult()
    
    def getIntegerValue(value: int = 0):
        dialog = QDialogService.QIntegerInputDialog(value = value)
        code = dialog.exec()
        return None if code != QDialogService.Response.ACCEPT else dialog.getResult()
    
    def getStyle(data: dict, style: str) -> str:
        dialog = QDialogService.QStyleListDialog(data = data, style = style)
        dialog.exec()
        return dialog.getResult()