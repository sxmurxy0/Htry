from PyQt6.QtCore import QFile, QIODeviceBase
from PyQt6.QtGui import QIcon, QPixmap, QFont
from enum import Enum
import resources

class Icons(Enum):
    LOGO = "logo.png"
    SEARCH = "search.png"
    ARROW_DOWN = "arrow_down.png"
    ARROW_UP = "arrow_up.png"
    FILE = "file.png"
    FOLDER = "folder.png"
    SAVE = "save.png"
    SAVE_AS = "save_as.png"
    CROSS = "cross.png"
    SCISSORS = "scissors.png"
    COPY = "copy.png"
    PASTE = "paste.png"
    UNDO = "undo.png"
    REDO = "redo.png"
    BOLD = "bold.png"
    ITALIC = "italic.png"
    UNDERLINED = "underlined.png"
    STRIKETHROUGH = "strikethrough.png"
    PICKER = "picker.png"
    FILLING = "filling.png"
    SPACING = "spacing.png"
    INDENTATION = "indentation.png"
    PICTURE = "picture.png"
    LINK = "link.png"

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