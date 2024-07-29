from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QGridLayout, QFontComboBox,
    QSpinBox, QPushButton, QLabel, QButtonGroup)
from PyQt6.QtCore import Qt
from widgets import Utility
from resources.Icons import *
from resources import ResourceProvider
from Binder import *
from typing import Iterable

class QHotbar(QFrame):

    class QCategory(QFrame):

        def __init__(self, parent: QWidget, title: str) -> None:
            super().__init__(parent)

            layout = QGridLayout(self)
            layout.setContentsMargins(13, 13, 14, 2)
            layout.setHorizontalSpacing(8)
            layout.setVerticalSpacing(6)
            self.setLayout(layout)

            self.titleLabel = QLabel(parent = self, text = title)
            self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout().addWidget(self.titleLabel, 1, 0, 1, -1)
        
        def addWidget(self, widget: QWidget) -> None:
            column = self.layout().count() - 1
            self.layout().addWidget(widget, 0, column)
        
        def addWidgets(self, widgets: Iterable[QWidget]) -> None:
            for widget in widgets:
                self.addWidget(widget)
    
    def __init__(self, parent: QWidget, binder: Binder) -> None:
        super().__init__(parent)

        self.setFixedHeight(76)
        self.setStyleSheet(ResourceProvider.loadStyleSheet("hotbar"))

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

        Utility.addHorizontalSpacer(self)
    
    def setupFontCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Шрифт")

        fontInput = QFontComboBox(parent = category)
        fontInput.setFixedSize(150, 28)
        fontInput.currentFontChanged.connect(binder.hotbarFontBinding.emit)
        binder.cursorFontBinding.connect(fontInput.setCurrentFont)
        category.fontInput = fontInput

        fontSizeInput = QSpinBox(parent = category)
        fontSizeInput.setFixedSize(50, 28)
        fontSizeInput.setRange(1, 72)
        fontSizeInput.valueChanged.connect(binder.hotbarFontSizeBinding.emit)
        binder.cursorFontSizeBinding.connect(fontSizeInput.setValue)
        category.fontSizeInput = fontSizeInput

        category.addWidgets((fontInput, fontSizeInput))
        
        self.layout().addWidget(category)
        self.fontCategory = category

        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupFormatCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Формат")

        boldButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.BOLD))
        Utility.setButtonParameters(boldButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        boldButton.toggled.connect(binder.hotbarBoldBinding.emit)
        binder.cursorBoldBinding.connect(boldButton.setChecked)
        category.boldButton = boldButton

        italicButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.ITALIC))
        Utility.setButtonParameters(italicButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        italicButton.toggled.connect(binder.hotbarItalicBinding.emit)
        binder.cursorItalicBinding.connect(italicButton.setChecked)
        category.italicButton = italicButton

        underlineButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.UNDERLINE))
        Utility.setButtonParameters(underlineButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        underlineButton.toggled.connect(binder.hotbarUnderlineBinding.emit)
        binder.cursorUnderlineBinding.connect(underlineButton.setChecked)
        category.underlineButton = underlineButton
        
        strikethroughButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.STRIKETHROUGH))
        Utility.setButtonParameters(strikethroughButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        strikethroughButton.toggled.connect(binder.hotbarStrikethroughBinding.emit)
        binder.cursorStrikethroughBinding.connect(strikethroughButton.setChecked)
        category.strikethroughButton = strikethroughButton

        category.addWidgets((boldButton, italicButton, underlineButton, strikethroughButton))

        self.layout().addWidget(category)
        self.formatCategory = category

        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupColorCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Цвет")

        textColorButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.PICKER))
        Utility.setButtonParameters(textColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18, checkable = True)
        category.textColorButton = textColorButton
        
        bgColorButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.FILLING))
        Utility.setButtonParameters(bgColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18, checkable = True)
        category.bgColorButton = bgColorButton

        category.addWidgets((textColorButton, bgColorButton))

        self.layout().addWidget(category)
        self.colorCategory = category
        
        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupAlignCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Выравнивание")
        category.group = QButtonGroup(category)

        alignLeftButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.ALIGN_LEFT))
        alignLeftButton.alignment = Qt.AlignmentFlag.AlignLeft
        Utility.setButtonParameters(alignLeftButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignLeftButton)
        category.alignLeftButton = alignLeftButton

        alignCenterButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.ALIGN_CENTER))
        alignCenterButton.alignment = Qt.AlignmentFlag.AlignCenter
        Utility.setButtonParameters(alignCenterButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignCenterButton)
        category.alignCenterButton = alignCenterButton

        alignRightButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.ALIGN_RIGHT))
        alignRightButton.alignment = Qt.AlignmentFlag.AlignRight
        Utility.setButtonParameters(alignRightButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignRightButton)
        category.alignRightButton = alignRightButton

        alignJustifyButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.ALIGN_JUSTIFY))
        alignJustifyButton.alignment = Qt.AlignmentFlag.AlignJustify
        Utility.setButtonParameters(alignJustifyButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignJustifyButton)
        category.alignJustifyButton = alignJustifyButton

        category.group.buttonClicked.connect(
            lambda button: binder.hotbarAlignmentBinding.emit(button.alignment)
        )
        binder.cursorAlignmentBinding.connect(self.handleCursorAlignment)

        category.addWidgets((alignLeftButton, alignCenterButton, alignRightButton, alignJustifyButton))

        self.layout().addWidget(category)
        self.alignmentCategory = category

        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupInsertionCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Вставка")

        pictureButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.PICTURE))
        Utility.setButtonParameters(pictureButton, width = 28, height = 28,
            iconWidth = 22, iconHeight = 22, checkable = True)
        pictureButton.clicked.connect(binder.insertPictureBinding.emit)
        category.pictureButton = pictureButton

        linkButton = QPushButton(parent = category,
            icon = ResourceProvider.getIcon(Icons.LINK))
        Utility.setButtonParameters(linkButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18, checkable = True)
        linkButton.clicked.connect(binder.insertLinkBindng.emit)
        category.linkButton = linkButton
        
        category.addWidgets((pictureButton, linkButton))

        self.layout().addWidget(category)
        self.insertionCategory = category
        
        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def setupParagraphCategory(self, binder: Binder) -> None:
        category = QHotbar.QCategory(parent = self, title = "Абзац")

        spacingButton = QPushButton(icon = ResourceProvider.getIcon(Icons.SPACING))
        Utility.setButtonParameters(spacingButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.spacingButton = spacingButton

        indentationButton = QPushButton(icon = ResourceProvider.getIcon(Icons.INDENTATION))
        Utility.setButtonParameters(indentationButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.indentationButton = indentationButton

        category.addWidgets((spacingButton, indentationButton))

        self.layout().addWidget(category)
        self.paragraphCategory = category
        
        Utility.addVerticalSeparator(widget = self, height = 62)
    
    def handleCursorAlignment(self, alignment: Qt.AlignmentFlag):
        for button in self.alignmentCategory.group.buttons():
            if button.alignment == alignment:
                button.setChecked(True)