from PyQt6.QtCore import QFile, QIODeviceBase
from PyQt6.QtGui import QIcon, QPixmap
from resources.QIcons import QIcons
import typing
        
class QResourceProvider:

    ICONS_CACHE = {}
    STYLES_CACHE = {}

    @staticmethod
    def loadIcon(fileName: str) -> QIcon:
        icon = QIcon()

        normalFilePath = "icons:" + fileName
        i = normalFilePath.rfind(".")
        disabledFilePath = normalFilePath[:i] + "_disabled" + normalFilePath[i:]

        if QFile.exists(normalFilePath):
            icon.addPixmap(QPixmap(normalFilePath), mode = QIcon.Mode.Normal)
        if QFile.exists(disabledFilePath):
            icon.addPixmap(QPixmap(disabledFilePath), mode = QIcon.Mode.Disabled)
        
        return icon

    @staticmethod
    def getIcon(icon: QIcons) -> QIcon:
        if icon not in QResourceProvider.ICONS_CACHE:
            QResourceProvider.ICONS_CACHE[icon] = QResourceProvider.loadIcon(icon.value)
        
        return QResourceProvider.ICONS_CACHE[icon]

    @staticmethod
    def loadStyleSheet(fileName: str) -> str:
        filePath = "styles:" + fileName
        
        if not QFile.exists(filePath):
            return ""

        file = QFile(filePath)
        file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text)
        styleSheet = str(file.readAll(), encoding = "utf-8")
        file.close()

        return styleSheet

    @staticmethod
    def getStyleSheet(identifier: str) -> str:
        if identifier not in QResourceProvider.STYLES_CACHE:
            QResourceProvider.STYLES_CACHE[identifier] = QResourceProvider.loadStyleSheet(identifier + ".qss")
            
        return QResourceProvider.STYLES_CACHE[identifier]
    
    @staticmethod
    def getMergedStyleSheet(identifiers: typing.Iterable[str]) -> str:
        styleSheet = ""
        for identifier in identifiers:
            styleSheet += QResourceProvider.getStyleSheet(identifier) + "\n"
        
        return styleSheet