from PyQt6.QtWidgets import (QWidget, QFrame, QHBoxLayout, QGridLayout,
    QFontComboBox, QSpinBox, QPushButton, QLabel, QButtonGroup)
from PyQt6.QtGui import QIcon, QPainter, QColor, QPaintEvent, QMouseEvent
from PyQt6.QtCore import Qt, QFile
from widgets.QWidgetUtility import QWidgetUtility
from widgets.QDialogService import QDialogService
from resources.QIcons import QIcons
from resources.QResourceProvider import QResourceProvider
from QBinder import QBinder
import typing, json, os

class QHotbar(QFrame):
        
    class QHotbarButton(QPushButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None) -> None:
            super().__init__(parent = parent, text = text)
            if icon:
                self.setIcon(icon)
    
    class QHotbarColorButton(QHotbarButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None, 
                color: QColor = QColor("#ffffff")) -> None:
            super().__init__(parent = parent, text = text, icon = icon)
            self.color = color
        
        def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.RightButton:
                color = QDialogService.getColor(self.color)
                if color != None:
                    self.color = color
                    self.clicked.emit()
        
        def setColor(self, color: QColor) -> None:
            self.color = color
        
        def paintEvent(self, event: QPaintEvent) -> None:
            super().paintEvent(event)

            painter = QPainter(self)
            painter.setPen(self.color)
            painter.setBrush(self.color)
            painter.drawRect(1, self.height() - 2, self.width() - 2, 2)
            painter.end()
    
    class QHotbarIntegerButton(QHotbarButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None, value: int = 0) -> None:
            super().__init__(parent = parent, text = text, icon = icon)
            self.value = value
        
        def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.RightButton:
                value = QDialogService.getIntegerValue(value = self.value)
                if value != None:
                    self.value = value
                    self.clicked.emit()
        
        def setValue(self, value: int) -> None:
            self.value = value
    
    class QHotbarStyleButton(QHotbarButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None) -> None:
            super().__init__(parent = parent, text = text, icon = icon)
            self.filePath = os.getenv('APPDATA') + "\config.json"
            self.data = {}
            self.style = ''

            self.readConfig()
    
        def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
            if event.button() == Qt.MouseButton.RightButton:
                self.style = QDialogService.getStyle(data = self.data,
                    style = self.style)
                self.writeConfig()
                self.clicked.emit()
                
        def readConfig(self) -> None:
            if not QFile.exists(self.filePath):
                return
            with open(self.filePath, "r") as config:
                self.data = json.load(config)
                if self.data and len(self.data) > 0:
                    self.style = list(self.data.keys())[0]
                elif not self.data:
                    self.data = {}

        def writeConfig(self) -> None:
            with open(self.filePath, "w") as config:
                json.dump(self.data, config, ensure_ascii = False)

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
            self.layout().addWidget(widget, 0, column, Qt.AlignmentFlag.AlignHCenter)
        
        def addWidgets(self, widgets: typing.Iterable[QWidget]) -> None:
            for widget in widgets:
                self.addWidget(widget)
    
    def __init__(self, parent: QWidget, binder: QBinder, styleMode = False) -> None:
        super().__init__(parent)

        self.setFixedHeight(76)
        self.setStyleSheet(QResourceProvider.getStyleSheet("hotbar"))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.setLayout(layout)

        self.binder = binder

        self.setupFontCategory()
        self.setupFormatCategory()
        self.setupColorCategory()
        self.setupAlignCategory()
        if not styleMode:
            self.setupInsertionCategory()
        self.setupParagraphCategory()
        if not styleMode:
            self.setupStyleCategory()

        QWidgetUtility.addHorizontalSpacer(self)
    
    def setupFontCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Шрифт")

        fontInput = QFontComboBox(parent = category)
        fontInput.setStyleSheet(QResourceProvider.getStyleSheet("font_combo_box"))
        fontInput.setFixedSize(150, 28)
        fontInput.currentFontChanged.connect(self.binder.hotbarFontBinding.emit)
        self.binder.cursorFontBinding.connect(fontInput.setCurrentFont)
        category.fontInput = fontInput

        QWidgetUtility.hackFontComboBox(fontInput)

        fontSizeInput = QSpinBox(parent = category)
        fontSizeInput.setFixedSize(50, 28)
        fontSizeInput.setRange(1, 72)
        fontSizeInput.editingFinished.connect(
            lambda: self.binder.hotbarFontSizeBinding.emit(fontSizeInput.value()))
        self.binder.cursorFontSizeBinding.connect(fontSizeInput.setValue)
        category.fontSizeInput = fontSizeInput
        
        category.addWidgets((fontInput, fontSizeInput))
        
        self.layout().addWidget(category)
        self.fontCategory = category

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupFormatCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Формат")

        boldButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.BOLD))
        QWidgetUtility.setButtonParameters(boldButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        boldButton.toggled.connect(self.binder.hotbarBoldBinding.emit)
        self.binder.cursorBoldBinding.connect(boldButton.setChecked)
        category.boldButton = boldButton

        italicButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ITALIC))
        QWidgetUtility.setButtonParameters(italicButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        italicButton.toggled.connect(self.binder.hotbarItalicBinding.emit)
        self.binder.cursorItalicBinding.connect(italicButton.setChecked)
        category.italicButton = italicButton

        underlineButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.UNDERLINE))
        QWidgetUtility.setButtonParameters(underlineButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        underlineButton.toggled.connect(self.binder.hotbarUnderlineBinding.emit)
        self.binder.cursorUnderlineBinding.connect(underlineButton.setChecked)
        category.underlineButton = underlineButton
        
        strikethroughButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.STRIKEOUT))
        QWidgetUtility.setButtonParameters(strikethroughButton, width = 28, height = 28,
            iconWidth = 16, iconHeight = 16, checkable = True)
        strikethroughButton.toggled.connect(self.binder.hotbarStrikeoutBinding.emit)
        self.binder.cursorStrikeoutBinding.connect(strikethroughButton.setChecked)
        category.strikethroughButton = strikethroughButton

        resetButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.ERASER))
        resetButton.clicked.connect(self.binder.resetFormatBinding)
        QWidgetUtility.setButtonParameters(resetButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18)
        category.resetButton = resetButton

        category.addWidgets((boldButton, italicButton, underlineButton, strikethroughButton, resetButton))

        self.layout().addWidget(category)
        self.formatCategory = category

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupColorCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Цвет")

        textColorButton = QHotbar.QHotbarColorButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.PICKER), color = QColor("#00000"))
        QWidgetUtility.setButtonParameters(textColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18)
        textColorButton.clicked.connect(self.handleTextColorButtonClick)
        category.textColorButton = textColorButton
        
        bgColorButton = QHotbar.QHotbarColorButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.FILLING), color = QColor("#ffffff"))
        QWidgetUtility.setButtonParameters(bgColorButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18)
        bgColorButton.clicked.connect(self.handleBgColorButtonClick)
        category.bgColorButton = bgColorButton

        category.addWidgets((textColorButton, bgColorButton))

        self.layout().addWidget(category)
        self.colorCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupAlignCategory(self) -> None:
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
            lambda button: self.binder.hotbarAlignmentBinding.emit(button.alignment))
        self.binder.cursorAlignmentBinding.connect(self.handleCursorAlignment)

        category.addWidgets((alignLeftButton, alignCenterButton, alignRightButton, alignJustifyButton))

        self.layout().addWidget(category)
        self.alignmentCategory = category

        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupInsertionCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Вставка")

        pictureButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.IMAGE))
        QWidgetUtility.setButtonParameters(pictureButton, width = 28, height = 28,
            iconWidth = 22, iconHeight = 22)
        pictureButton.clicked.connect(self.binder.insertImageBinding.emit)
        category.pictureButton = pictureButton

        linkButton = QHotbar.QHotbarButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.LINK))
        QWidgetUtility.setButtonParameters(linkButton, width = 28, height = 28,
            iconWidth = 18, iconHeight = 18)
        linkButton.clicked.connect(self.binder.insertLinkBindng.emit)
        category.linkButton = linkButton
        
        category.addWidgets((pictureButton, linkButton))

        self.layout().addWidget(category)
        self.insertionCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupParagraphCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Абзац")

        spacingButton = QHotbar.QHotbarIntegerButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.SPACING))
        QWidgetUtility.setButtonParameters(spacingButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20)
        spacingButton.clicked.connect(self.handleSpacingButtonClick)
        self.binder.cursorSpacingBinding.connect(spacingButton.setValue)
        category.spacingButton = spacingButton

        indentationButton = QHotbar.QHotbarIntegerButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.INDENTATION))
        QWidgetUtility.setButtonParameters(indentationButton, width = 28, height = 28,
            iconWidth = 20, iconHeight = 20)
        indentationButton.clicked.connect(self.handleIndentationButtonClick)
        self.binder.cursorIndentationBinding.connect(indentationButton.setValue)
        category.indentationButton = indentationButton

        category.addWidgets((spacingButton, indentationButton))

        self.layout().addWidget(category)
        self.paragraphCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def setupStyleCategory(self) -> None:
        category = QHotbar.QHotbarCategory(parent = self, title = "Стиль")

        styleButton = QHotbar.QHotbarStyleButton(parent = category,
            icon = QResourceProvider.getIcon(QIcons.STYLE))
        QWidgetUtility.setButtonParameters(styleButton, width = 28, height = 28,
            iconWidth = 22, iconHeight = 22)
        styleButton.clicked.connect(self.handleStyleButtonClick)
        category.styleButton = styleButton

        category.addWidget(styleButton)

        self.layout().addWidget(category)
        self.styleCategory = category
        
        QWidgetUtility.addVerticalSeparator(widget = self, height = 62)
    
    def handleTextColorButtonClick(self) -> None:
        self.binder.textColorBinding.emit(
            self.colorCategory.textColorButton.color)
    
    def handleBgColorButtonClick(self) -> None:
        self.binder.bgColorBinding.emit(
            self.colorCategory.bgColorButton.color)
    
    def handleSpacingButtonClick(self) -> None:
        self.binder.hotbarSpacingBinding.emit(
            self.paragraphCategory.spacingButton.value)  
        
    def handleIndentationButtonClick(self) -> None:
        self.binder.hotbarIndentationBinding.emit(
            self.paragraphCategory.indentationButton.value)
    
    def handleCursorAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        for button in self.alignmentCategory.group.buttons():
            if button.alignment == alignment:
                button.setChecked(True)
    
    def handleStyleButtonClick(self) -> None:
        style = self.styleCategory.styleButton.style
        if style:
            self.binder.applyStyleBinding.emit(self.styleCategory.styleButton.data[style])
        else:
            self.binder.applyStyleBinding.emit({})