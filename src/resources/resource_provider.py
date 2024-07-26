from PyQt6.QtCore import QFile, QIODeviceBase
from PyQt6.QtGui import QIcon, QPixmap, QFont
from resources.icons import Icons
import resources.data

icons_cache = {}

def getIcon(icon: Icons) -> QIcon:
    if icon not in icons_cache:
        icons_cache[icon] = QIcon(QPixmap(f":/icons/{icon.value}"))
    
    return icons_cache[icon]

def getStyleSheet(identifier: str) -> str:
    file = QFile(f":/styles/{identifier}.qss")
    
    if not file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text):
        return ""
    
    style_sheet = str(file.readAll(), encoding = "utf-8")
    file.close()

    return style_sheet