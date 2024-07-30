from PyQt6.QtCore import QFile, QIODeviceBase
from PyQt6.QtGui import QIcon, QPixmap
from core.resources.Icons import Icons
        
iconsCache = {}
stylesCache = {}

def loadIcon(fileName: str) -> QIcon:
    icon = QIcon()

    normal_path = f"icons:{fileName}"
    i = normal_path.rfind(".")
    disabled_path = normal_path[:i] + "_disabled" + normal_path[i:]

    if QFile.exists(normal_path):
        icon.addPixmap(QPixmap(normal_path), mode = QIcon.Mode.Normal)
    if QFile.exists(disabled_path):
        icon.addPixmap(QPixmap(disabled_path), mode = QIcon.Mode.Disabled)
    
    return icon

def getIcon(icon: Icons) -> QIcon:
    if icon not in iconsCache:
        iconsCache[icon] = loadIcon(icon.value)
    
    return iconsCache[icon]

def loadStyleSheet(fileName: str) -> str:
    path = f"styles:{fileName}"
    
    if not QFile.exists(path):
        return ""

    file = QFile(path)
    file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text)
    styleSheet = str(file.readAll(), encoding = "utf-8")
    file.close()

    return styleSheet

def getStyleSheet(identifier: str) -> str:
    if identifier not in stylesCache:
        stylesCache[identifier] = loadStyleSheet(identifier + ".qss")
        
    return stylesCache[identifier]