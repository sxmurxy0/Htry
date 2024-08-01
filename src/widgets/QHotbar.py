from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QGridLayout,
    QFontComboBox, QSpinBox, QPushButton, QLabel, QButtonGroup)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from widgets.QWidgetUtility import QWidgetUtility
from resources.QIcons import QIcons
from resources.QResourceProvider import QResourceProvider
from QBinder import QBinder
import typing

class QHotbar(QFrame):

    class QHotbarButton(QPushButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None) -> None:
            super().__init__(parent = parent, text = text)
            if icon:
                self.setIcon(icon)

    class QHotbarCategory(QFrame):

        def __init__(self, parent: QWidget, title: str) -> None:
            super().__init__(parent)

            layout = QGridLayout(self)
            layout.setContentsMargins(13, 13, 14, 2)
            layout.setHorizontalSpacing(8)
            layout.setVerticalSpacing(6)
            self.setLayout(layout)

            self.titleLabel = QLabel(parent = self, text = title)
            self.titleLabel.setProperty("category_title", True)
            self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout().addWidget(self.titleLabel, 1, 0, 1, -1)
        
        def addWidget(self, widget: QWidget) -> None:
            column = self.layout().count() - 1
            self.layout().addWidget(widget, 0, column)
        
        def addWidgets(self, widgets: typing.Iterable[QWidget]) -> None:
            for widget in widgets:
                self.addWidget(widget)
    
    def __init__(self, parent: QWidget, binder: QBinder) -> None:
        super().__init__(parent)

        self.setFixedHeight(76)
        self.setStyleSheet(QResourceProvider.getStyleSheet("hotbar"))

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

        QWidgetUtility.addHorizontalSpacer(self)
    
    def setupFontCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Шрифт")

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

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupFormatCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Формат")

        boldButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.BOLD))
        QWidgetUtility.setButtonParameters(boldButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        boldButton.toggled.connect(binder.hotbarBoldBinding.emit)
        binder.cursorBoldBinding.connect(boldButton.setChecked)
        category.boldButton = boldButton

        italicButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ITALIC))
        QWidgetUtility.setButtonParameters(italicButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        italicButton.toggled.connect(binder.hotbarItalicBinding.emit)
        binder.cursorItalicBinding.connect(italicButton.setChecked)
        category.italicButton = italicButton

        underlineButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.UNDERLINE))
        QWidgetUtility.setButtonParameters(underlineButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        underlineButton.toggled.connect(binder.hotbarUnderlineBinding.emit)
        binder.cursorUnderlineBinding.connect(underlineButton.setChecked)
        category.underlineButton = underlineButton
        
        strikethroughButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.STRIKETHROUGH))
        QWidgetUtility.setButtonParameters(strikethroughButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        strikethroughButton.toggled.connect(binder.hotbarStrikethroughBinding.emit)
        binder.cursorStrikethroughBinding.connect(strikethroughButton.setChecked)
        category.strikethroughButton = strikethroughButton

        category.addWidgets((boldButton, italicButton, underlineButton, strikethroughButton))

        self.layout().addWidget(category)
        self.formatCategory = category

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupColorCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Цвет")

        textColorButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.PICKER))
        QWidgetUtility.setButtonParameters(textColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18, checkable = True)
        category.textColorButton = textColorButton
        
        bgColorButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.FILLING))
        QWidgetUtility.setButtonParameters(bgColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18, checkable = True)
        category.bgColorButton = bgColorButton

        category.addWidgets((textColorButton, bgColorButton))

        self.layout().addWidget(category)
        self.colorCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupAlignCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Выравнивание")
        category.group = QButtonGroup(category)

        alignLeftButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ALIGN_LEFT))
        alignLeftButton.alignment = Qt.AlignmentFlag.AlignLeft
        QWidgetUtility.setButtonParameters(alignLeftButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignLeftButton)
        category.alignLeftButton = alignLeftButton

        alignCenterButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ALIGN_CENTER))
        alignCenterButton.alignment = Qt.AlignmentFlag.AlignCenter
        QWidgetUtility.setButtonParameters(alignCenterButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignCenterButton)
        category.alignCenterButton = alignCenterButton

        alignRightButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ALIGN_RIGHT))
        alignRightButton.alignment = Qt.AlignmentFlag.AlignRight
        QWidgetUtility.setButtonParameters(alignRightButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignRightButton)
        category.alignRightButton = alignRightButton

        alignJustifyButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ALIGN_JUSTIFY))
        alignJustifyButton.alignment = Qt.AlignmentFlag.AlignJustify
        QWidgetUtility.setButtonParameters(alignJustifyButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.group.addButton(alignJustifyButton)
        category.alignJustifyButton = alignJustifyButton

        category.group.buttonClicked.connect(
            lambda button: binder.hotbarAlignmentBinding.emit(button.alignment))
        binder.cursorAlignmentBinding.connect(self.handleCursorAlignment)

        category.addWidgets((alignLeftButton, alignCenterButton, alignRightButton, alignJustifyButton))

        self.layout().addWidget(category)
        self.alignmentCategory = category

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupInsertionCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Вставка")

        pictureButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.PICTURE))
        QWidgetUtility.setButtonParameters(pictureButton, width = 28, height = 28,
            iconWidth = 22, iconHeight = 22)
        pictureButton.clicked.connect(binder.insertPictureBinding.emit)
        category.pictureButton = pictureButton

        linkButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.LINK))
        QWidgetUtility.setButtonParameters(linkButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18)
        linkButton.clicked.connect(binder.insertLinkBindng.emit)
        category.linkButton = linkButton
        
        category.addWidgets((pictureButton, linkButton))

        self.layout().addWidget(category)
        self.insertionCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupParagraphCategory(self, binder: QBinder) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Абзац")

        spacingButton = QHotbar.QHotbarButton(icon = QResourceProvider.getIcon(QIcons.SPACING))
        QWidgetUtility.setButtonParameters(spacingButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.spacingButton = spacingButton

        indentationButton = QHotbar.QHotbarButton(icon = QResourceProvider.getIcon(QIcons.INDENTATION))
        QWidgetUtility.setButtonParameters(indentationButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20, checkable = True)
        category.indentationButton = indentationButton

        category.addWidgets((spacingButton, indentationButton))

        self.layout().addWidget(category)
        self.paragraphCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def handleCursorAlignment(self, alignment: Qt.AlignmentFlag):
        for button in self.alignmentCategory.group.buttons():
            if button.alignment == alignment:
                button.setChecked(True)