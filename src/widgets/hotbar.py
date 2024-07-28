from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QGridLayout, 
    QFontComboBox, QSpinBox, QPushButton, QLabel, QButtonGroup)
from PyQt6.QtCore import Qt, QSize, QObject
from widgets import utility
from resources.icons import Icons
from resources import resource_provider
from binder import Binder
from typing import Iterable

class QHotbar(QFrame):

    class QCategory(QFrame):

        def __init__(self, parent: QWidget, title: str) -> None:
            super().__init__(parent)

            layout = QGridLayout(self)
            layout.setContentsMargins(13, 13, 14, 2)
            layout.setSpacing(8)
            layout.setVerticalSpacing(6)
            self.setLayout(layout)

            self.title_label = QLabel(parent = self, text = title)
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout().addWidget(self.title_label, 1, 0, 1, -1)
        
        def addWidget(self, widget: QWidget) -> None:
            column = self.layout().count() - 1
            self.layout().addWidget(widget, 0, column)
        
        def addWidgets(self, widgets: Iterable[QWidget]) -> None:
            for widget in widgets:
                self.addWidget(widget)
    
    def __init__(self, parent: QWidget, binder: Binder) -> None:
        super().__init__(parent)

        self.setFixedHeight(76)
        self.setStyleSheet(resource_provider.getStyleSheet("hotbar"))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.setLayout(layout)

        self.setupFontCategory(binder)
        self.setupFormatCategory(binder)
        self.setupColorCategory(binder)
        self.setupAlignCategory(binder)
        self.setupInsertionCategory(binder)
        self.setupParagraphCategory(binder)

        utility.addHorizontalSpacer(self)
    
    def setupFontCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Шрифт")

        font_input = QFontComboBox(parent = category)
        font_input.setFixedSize(150, 28)
        font_input.currentFontChanged.connect(binder.hotbar_font_binding.emit)
        binder.cursor_font_binding.connect(font_input.setCurrentFont)
        category.font_input = font_input

        font_size_input = QSpinBox(parent = category)
        font_size_input.setFixedSize(50, 28)
        font_size_input.setRange(1, 72)
        font_size_input.valueChanged.connect(binder.hotbar_font_size_binding.emit)
        binder.cursor_font_size_binding.connect(font_size_input.setValue)
        category.font_size_input = font_size_input

        category.addWidgets((font_input, font_size_input))
        
        self.layout().addWidget(category)
        self.font_category = category

        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupFormatCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Формат")

        bold_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.BOLD))
        utility.setButtonParameters(bold_button, width = 28, height = 28,
            icon_width = 16, icon_height = 16, checkable = True)
        bold_button.toggled.connect(binder.hotbar_bold_binding.emit)
        binder.cursor_bold_binding.connect(bold_button.setChecked)
        category.bold_button = bold_button

        italic_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.ITALIC))
        utility.setButtonParameters(italic_button, width = 28, height = 28,
            icon_width = 16, icon_height = 16, checkable = True)
        italic_button.toggled.connect(binder.hotbar_italic_binding.emit)
        binder.cursor_italic_binding.connect(italic_button.setChecked)
        category.italic_button = italic_button

        underline_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.UNDERLINE))
        utility.setButtonParameters(underline_button, width = 28, height = 28,
            icon_width = 16, icon_height = 16, checkable = True)
        underline_button.toggled.connect(binder.hotbar_underline_binding.emit)
        binder.cursor_underline_binding.connect(underline_button.setChecked)
        category.underline_button = underline_button
        
        strikethrough_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.STRIKETHROUGH))
        utility.setButtonParameters(strikethrough_button, width = 28, height = 28,
            icon_width = 16, icon_height = 16, checkable = True)
        strikethrough_button.toggled.connect(binder.hotbar_strikethrough_binding.emit)
        binder.cursor_strikethrough_binding.connect(strikethrough_button.setChecked)
        category.strikethrough_button = strikethrough_button

        category.addWidgets((bold_button, italic_button, underline_button, strikethrough_button))

        self.layout().addWidget(category)
        self.format_category = category

        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupColorCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Цвет")

        text_color_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.PICKER))
        utility.setButtonParameters(text_color_button, width = 28, height = 28,
            icon_width = 18, icon_height = 18, checkable = True)
        category.text_color_button = text_color_button
        
        bg_color_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.FILLING))
        utility.setButtonParameters(bg_color_button, width = 28, height = 28,
            icon_width = 18, icon_height = 18, checkable = True)
        category.bg_color_button = bg_color_button

        category.addWidgets((text_color_button, bg_color_button))

        self.layout().addWidget(category)
        self.color_category = category
        
        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupAlignCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Выравнивание")
        category.group = QButtonGroup(category)

        align_left_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.ALIGN_LEFT))
        align_left_button.alignment = Qt.AlignmentFlag.AlignLeft
        utility.setButtonParameters(align_left_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.group.addButton(align_left_button)
        category.align_left_button = align_left_button

        align_center_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.ALIGN_CENTER))
        align_center_button.alignment = Qt.AlignmentFlag.AlignCenter
        utility.setButtonParameters(align_center_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.group.addButton(align_center_button)
        category.align_center_button = align_center_button

        align_right_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.ALIGN_RIGHT))
        align_right_button.alignment = Qt.AlignmentFlag.AlignRight
        utility.setButtonParameters(align_right_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.group.addButton(align_right_button)
        category.align_right_button = align_right_button

        align_justify_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.ALIGN_JUSTIFY))
        align_justify_button.alignment = Qt.AlignmentFlag.AlignJustify
        utility.setButtonParameters(align_justify_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.group.addButton(align_justify_button)
        category.align_justify_button = align_justify_button

        category.group.buttonClicked.connect(
            lambda button: binder.hotbar_alignment_binding.emit(button.alignment)
        )
        binder.cursor_alignment_binding.connect(self.handleCursorAlignment)

        category.addWidgets((align_left_button, align_center_button, align_right_button, align_justify_button))

        self.layout().addWidget(category)
        self.alignment_category = category

        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupInsertionCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Вставка")

        picture_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.PICTURE))
        utility.setButtonParameters(picture_button, width = 28, height = 28,
            icon_width = 22, icon_height = 22, checkable = True)
        picture_button.clicked.connect(binder.insert_picture_binding.emit)
        category.picture_button = picture_button

        link_button = QPushButton(parent = category,
            icon = resource_provider.getIcon(Icons.LINK))
        utility.setButtonParameters(link_button, width = 28, height = 28,
            icon_width = 18, icon_height = 18, checkable = True)
        link_button.clicked.connect(binder.insert_link_bindng.emit)
        category.link_button = link_button
        
        category.addWidgets((picture_button, link_button))

        self.layout().addWidget(category)
        self.insertion_category = category
        
        utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupParagraphCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Абзац")

        spacing_button = QPushButton(icon = resource_provider.getIcon(Icons.SPACING))
        utility.setButtonParameters(spacing_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.spacing_button = spacing_button

        indentation_button = QPushButton(icon = resource_provider.getIcon(Icons.INDENTATION))
        utility.setButtonParameters(indentation_button, width = 28, height = 28,
            icon_width = 20, icon_height = 20, checkable = True)
        category.indentation_button = indentation_button

        category.addWidgets((spacing_button, indentation_button))

        self.layout().addWidget(category)
        self.paragraph_category = category
        
        utility.addVerticalSeparator(widget = self, height = 62)
    
    def handleCursorAlignment(self, alignment: Qt.AlignmentFlag):
        for button in self.alignment_category.group.buttons():
            if button.alignment == alignment:
                button.setChecked(True)