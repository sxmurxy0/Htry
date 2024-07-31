from PyQt6.QtCore import QFile, QIODeviceBase
from PyQt6.QtGui import QIcon, QPixmap
from resources.Icons import Icons
        
class QResourceProvider:

    ICONS_CACHE = {}
    STYLES_CACHE = {}

    @staticmethod
    def loadIcon(fileName: str) -> QIcon:
        icon = QIcon()

        normal_path = "icons:" + fileName
        i = normal_path.rfind(".")
        disabled_path = normal_path[:i] + "_disabled" + normal_path[i:]

        if QFile.exists(normal_path):
            icon.addPixmap(QPixmap(normal_path), mode = QIcon.Mode.Normal)
        if QFile.exists(disabled_path):
            icon.addPixmap(QPixmap(disabled_path), mode = QIcon.Mode.Disabled)
        
        return icon

    @staticmethod
    def getIcon(icon: Icons) -> QIcon:
        if icon not in QResourceProvider.ICONS_CACHE:
            QResourceProvider.ICONS_CACHE[icon] = QResourceProvider.loadIcon(icon.value)
        
        return QResourceProvider.ICONS_CACHE[icon]

    @staticmethod
    def loadStyleSheet(fileName: str) -> str:
        path = "styles:" + fileName
        
        if not QFile.exists(path):
            return ""

        file = QFile(path)
        file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text)
        styleSheet = str(file.readAll(), encoding = "utf-8")
        file.close()

        return styleSheet

    @staticmethod
    def getStyleSheet(identifier: str) -> str:
        if identifier not in QResourceProvider.STYLES_CACHE:
            QResourceProvider.STYLES_CACHE[identifier] = QResourceProvider.loadStyleSheet(identifier + ".qss")
            
        return QResourceProvider.STYLES_CACHE[identifier]