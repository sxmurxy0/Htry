from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QFontComboBox, QSpinBox, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from widgets import utility
from resources_provider import Icons
import resources_provider
from binder import Binder
from typing import Iterable

class QHotbar(QFrame):

    class QCategory(QFrame):

        def __init__(self, parent: QWidget, title: str, widgets: Iterable[QWidget]) -> None:
            super().__init__(parent)

            w = 14
            for widget in widgets:
                widget.setParent(self)
                widget.move(w, 14)
                w += widget.width() + 8
            w += 5 + w % 2
            
            self.setFixedSize(w, 76)

            self.title_label = QLabel(parent = self, text = title)
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.title_label.setGeometry(0, 50, w, 21)
    
    def __init__(self, parent: QWidget, binder: Binder) -> None:
        super().__init__(parent)

        self.setFixedHeight(76)
        self.setStyleSheet(resources_provider.getStyleSheet("hotbar"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.setLayout(layout)

        self.setupFontCategory(binder)
        self.setupFormatCategory(binder)
        self.setupColorCategory(binder)
        self.setupParagraphCategory(binder)
        self.setupInsertionCategory(binder)

        utility.addHorizontalSpacer(self)
    
    def setupFontCategory(self, binder: Binder) -> None:
        font_input = QFontComboBox()
        font_input.setFixedSize(130, 28)

        font_size_input = QSpinBox()
        font_size_input.setFixedSize(50, 28)
        font_size_input.setRange(1, 72)

        self.font_category = QHotbar.QCategory(parent = self, title = "Шрифт",
            widgets = (font_input, font_size_input))
        self.layout().addWidget(self.font_category)

        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupFormatCategory(self, binder: Binder) -> None:
        bold_button = QPushButton(icon = resources_provider.getIcon(Icons.BOLD))
        bold_button.setFixedSize(28, 28)
        bold_button.setIconSize(QSize(22, 22))
        bold_button.setCheckable(True)

        italic_button = QPushButton(icon = resources_provider.getIcon(Icons.ITALIC))
        italic_button.setFixedSize(28, 28)
        italic_button.setIconSize(QSize(22, 22))
        italic_button.setCheckable(True)

        underlined_button = QPushButton(icon = resources_provider.getIcon(Icons.UNDERLINED))
        underlined_button.setFixedSize(28, 28)
        underlined_button.setIconSize(QSize(22, 22))
        underlined_button.setCheckable(True)
        
        strikethrough_button = QPushButton(icon = resources_provider.getIcon(Icons.STRIKETHROUGH))
        strikethrough_button.setFixedSize(28, 28)
        strikethrough_button.setIconSize(QSize(22, 22))
        strikethrough_button.setCheckable(True)

        self.format_category = QHotbar.QCategory(parent = self, title = "Формат",
            widgets = (bold_button, italic_button, underlined_button, strikethrough_button))
        self.layout().addWidget(self.format_category)

        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupColorCategory(self, binder: Binder) -> None:
        text_color_button = QPushButton(icon = resources_provider.getIcon(Icons.PICKER))
        text_color_button.setFixedSize(28, 28)
        text_color_button.setIconSize(QSize(18, 18))
        text_color_button.setCheckable(True)
        
        background_color_button = QPushButton(icon = resources_provider.getIcon(Icons.FILLING))
        background_color_button.setFixedSize(28, 28)
        background_color_button.setIconSize(QSize(18, 18))
        background_color_button.setCheckable(True)
        
        self.color_category = QHotbar.QCategory(parent = self, title = "Цвет",
            widgets = (text_color_button, background_color_button))
        self.layout().addWidget(self.color_category)
        
        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupParagraphCategory(self, binder: Binder) -> None:
        spacing_button = QPushButton(icon = resources_provider.getIcon(Icons.SPACING))
        spacing_button.setFixedSize(28, 28)
        spacing_button.setIconSize(QSize(26, 26))
        spacing_button.setCheckable(True)

        indentation_button = QPushButton(icon = resources_provider.getIcon(Icons.INDENTATION))
        indentation_button.setFixedSize(28, 28)
        indentation_button.setIconSize(QSize(26, 26))
        indentation_button.setCheckable(True)

        self.paragraph_category = QHotbar.QCategory(parent = self, title = "Абзац",
            widgets = (spacing_button, indentation_button))
        self.layout().addWidget(self.paragraph_category)
        
        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupInsertionCategory(self, binder: Binder) -> None:
        picture_button = QPushButton(icon = resources_provider.getIcon(Icons.PICTURE))
        picture_button.setFixedSize(28, 28)
        picture_button.setIconSize(QSize(24, 24))
        picture_button.setCheckable(True)
        
        link_button = QPushButton(icon = resources_provider.getIcon(Icons.LINK))
        link_button.setFixedSize(28, 28)
        link_button.setIconSize(QSize(24, 24))
        link_button.setCheckable(True)
        
        self.insertion_category = QHotbar.QCategory(parent = self, title = "Вставка",
            widgets = (picture_button, link_button))
        self.layout().addWidget(self.insertion_category)
        
        utility.addVerticalSeparator(widget = self, height = 62)