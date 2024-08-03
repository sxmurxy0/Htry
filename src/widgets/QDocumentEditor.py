from PyQt6.QtWidgets import QWidget, QTextEdit, QMenu
from PyQt6.QtGui import (QTextFrameFormat, QTextBlockFormat, QTextImageFormat, QTextCharFormat,
     QKeyEvent, QPaintEvent, QFocusEvent, QMouseEvent, QDesktopServices, QPainter, QPen,
     QBrush, QColor, QAction, QKeySequence, QFont, QPixmap)
from PyQt6.QtCore import Qt, QSizeF, QPoint, QUrl
from widgets.QDialogService import QDialogService
from widgets.QWidgetUtility import QWidgetUtility
from resources.QIcons import QIcons
from resources.QResourceProvider import QResourceProvider
from documents.QDocument import QDocument
from QBinder import QBinder

class QDocumentEditor(QTextEdit):
    
    PAGE_WIDTH = 780
    PAGE_HEIGHT = 980
    PAGE_SIZE = QSizeF(PAGE_WIDTH, PAGE_HEIGHT)
    PAGE_PADDING = 50
    PAGE_SPACING = 30

    def __init__(self, parent: QWidget, binder: QBinder) -> None:
        super().__init__(parent)

        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        
        self.setFixedWidth(QDocumentEditor.PAGE_WIDTH)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.binder = binder
        self.updatingHotbar = False

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setupContextMenu()
        self.customContextMenuRequested.connect(self.openContextMenu)

        self.binder.undoBinding.connect(self.undo)
        self.binder.redoBinding.connect(self.redo)
        self.binder.cutBinding.connect(self.cut)
        self.binder.copyBinding.connect(self.copy)
        self.binder.pasteBinding.connect(self.paste)
        self.binder.selectAllBinding.connect(self.selectAll)

        self.undoAvailable.connect(self.binder.undoAvailableBinding.emit)
        self.redoAvailable.connect(self.binder.redoAvailableBinding.emit)
        self.copyAvailable.connect(self.binder.cutAvailableBinding.emit)
        self.copyAvailable.connect(self.binder.copyAvailableBinding.emit)

        self.binder.hotbarFontBinding.connect(self.setCurrentFont)
        self.binder.hotbarFontSizeBinding.connect(self.setFontPointSize)

        self.binder.hotbarBoldBinding.connect(self.setFontBold)
        self.binder.hotbarItalicBinding.connect(self.setFontItalic)
        self.binder.hotbarUnderlineBinding.connect(self.setFontUnderline)
        self.binder.hotbarStrikeoutBinding.connect(self.setFontStrikeout)

        self.binder.textColorBinding.connect(self.setTextColor)
        self.binder.bgColorBinding.connect(self.setBgColor)

        self.binder.hotbarAlignmentBinding.connect(self.setAlignment)

        self.binder.insertImageBinding.connect(self.insertPicture)
        self.binder.insertLinkBindng.connect(self.insertLink)

        self.binder.hotbarSpacingBinding.connect(self.setSpacing)
        self.binder.hotbarIndentationBinding.connect(self.setIndentation)
        self.binder.applyStyleBinding.connect(self.applyStyle)
        self.binder.resetFormatBinding.connect(self.resetFormat)

        self.binder.documentUpdatedBinding.connect(self.setDocument)

        self.cursorPositionChanged.connect(self.updateHotbarState)
        self.textChanged.connect(self.updateBounds)
    
    def focusInEvent(self, event: QFocusEvent) -> None:
        super().focusInEvent(event)
        self.ensureIfPasteAvailiable()
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        url = self.anchorAt(event.pos())
        if url:
            QDesktopServices.openUrl(QUrl(url))
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return \
            and event.keyCombination().keyboardModifiers() == Qt.KeyboardModifier.NoModifier:
            self.textCursor().insertBlock()
        else:
            super().keyPressEvent(event)
    
    def setCurrentFont(self, font: QFont) -> None:
        if not self.updatingHotbar:
            super().setCurrentFont(font)
            self.setFocus()
    
    def setFontPointSize(self, size: int) -> None:
        if not self.updatingHotbar:
            super().setFontPointSize(size)
            self.setFocus()
    
    def setFontBold(self, state: bool) -> None:
        if not self.updatingHotbar:
            super().setFontWeight(QFont.Weight.Bold if state else QFont.Weight.Normal)
            self.setFocus()
    
    def setFontItalic(self, state: bool) -> None:
        if not self.updatingHotbar:
            super().setFontItalic(state)
            self.setFocus()
    
    def setFontUnderline(self, state: bool) -> None:
        if not self.updatingHotbar:
            super().setFontUnderline(state)
            self.setFocus()
    
    def setFontStrikeout(self, state: bool) -> None:
        if not self.updatingHotbar:
            format = self.currentCharFormat()
            format.setFontStrikeOut(state)
            self.textCursor().mergeCharFormat(format)
            self.setFocus()
    
    def setTextColor(self, color: QColor) -> None:
        super().setTextColor(color)
        self.setFocus()

    def setBgColor(self, color: QColor) -> None:
        super().setTextBackgroundColor(color)
        self.setFocus()
    
    def setAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        if not self.updatingHotbar:
            super().setAlignment(alignment)
            self.setFocus()
    
    def applyStyle(self, style: dict) -> None:
        self.setFontPointSize(style["font_size"])
        self.setFontBold(style["bold"])
        self.setFontItalic(style["italic"])
        self.setFontUnderline(style["underline"])
        self.setFontStrikeout(style["strikeout"])
        self.setTextColor(QColor(style["text_color"]))
        self.setBgColor(QColor(style["bg_color"]))
        self.setSpacing(style["spacing"])
        self.setIndentation(style["indentation"])

        mode = {
            "center": Qt.AlignmentFlag.AlignCenter,
            "left": Qt.AlignmentFlag.AlignLeft,
            "right": Qt.AlignmentFlag.AlignRight,
            "justift": Qt.AlignmentFlag.AlignJustify
        }
        self.setAlignment(mode[style["alignment"]])

    def insertPicture(self) -> None:
        image = QDialogService.getImageInsertionFile()
        if image:
            url = QUrl(image)
            size = QDialogService.getImageSize(maxWidth = QDocumentEditor.PAGE_WIDTH,
                maxHeight = QDocumentEditor.PAGE_HEIGHT)

            pixmap = QPixmap(url.toString())
            self.document().addResource(QDocument.ResourceType.ImageResource, url, pixmap)

            format = QTextImageFormat()
            format.setWidth(size.width())
            format.setHeight(size.height())
            format.setName(url.toString())

            self.textCursor().insertImage(format)
            self.setFocus()
            
    def insertLink(self) -> None:
        title = self.textCursor().selectedText()
        data = QDialogService.getLinkInsertionData(title)
        
        if data and data[0]:
            format = self.currentCharFormat()
            format.setForeground(QColor(("#2d2dff")))
            format.setFontUnderline(True)
            format.setAnchor(True)
            format.setAnchorHref(data[1])
            self.textCursor().insertText(data[0], format)
            self.setFocus()
    
    def setSpacing(self, value: int) -> None:
        format = self.textCursor().blockFormat()
        format.setLineHeight(value, QTextBlockFormat.LineHeightTypes.LineDistanceHeight.value)
        self.textCursor().mergeBlockFormat(format)
        self.setFocus()
    
    def setIndentation(self, value: int) -> None:
        format = self.textCursor().blockFormat()
        format.setLeftMargin(value)
        self.textCursor().mergeBlockFormat(format)
        self.setFocus()
    
    def resetFormat(self) -> None:
        self.textCursor().setCharFormat(QTextCharFormat())
        self.setFocus()
    
    def updateHotbarState(self) -> None:
        self.updatingHotbar = True

        self.binder.cursorFontBinding.emit(self.currentFont())
        self.binder.cursorFontSizeBinding.emit(int(self.currentFont().pointSize()))
        self.binder.cursorBoldBinding.emit(self.currentFont().weight() == QFont.Weight.Bold)
        self.binder.cursorItalicBinding.emit(self.fontItalic())
        self.binder.cursorUnderlineBinding.emit(self.fontUnderline())
        self.binder.cursorStrikeoutBinding.emit(self.currentFont().strikeOut())
        self.binder.cursorAlignmentBinding.emit(self.alignment())

        self.updatingHotbar = False
    
    def ensureIfPasteAvailiable(self) -> None:
        self.binder.pasteAvailableBinding.emit(self.canPaste())
    
    def updateBounds(self):
        self.document().setPageSize(QDocumentEditor.PAGE_SIZE)
        self.setFixedHeight(self.document().pageCount() * QDocumentEditor.PAGE_HEIGHT)
    
    def setDocument(self, document: QDocument) -> None:
        super().setDocument(document)

        self.updateBounds()

        format = QTextFrameFormat()
        format.setMargin(QDocumentEditor.PAGE_PADDING)
        format.setBottomMargin(QDocumentEditor.PAGE_PADDING + QDocumentEditor.PAGE_SPACING)
        format.setBorder(1)
        format.setBorderBrush(QBrush(QColor("green"), Qt.BrushStyle.SolidPattern))
        
        self.document().rootFrame().setFrameFormat(format)
        self.document().setDefaultFont(QFont("Malgun Gothic", 9))
        
        self.document().setModified(False)
        self.document().clearUndoRedoStacks()

        self.updateHotbarState()
        self.setFocus()
        
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self.viewport())
        painter.setPen(QPen(QColor("#e6e3ed"), 1))
        painter.setBrush(QBrush(QColor("#ffffff"), Qt.BrushStyle.SolidPattern))
        
        width = QDocumentEditor.PAGE_WIDTH - 2
        height = QDocumentEditor.PAGE_HEIGHT - QDocumentEditor.PAGE_SPACING - 3

        for i in range(self.document().pageCount()):
            painter.drawRect(1, i * (QDocumentEditor.PAGE_HEIGHT) + 2, width, height)

        super().paintEvent(event)
    
    def openContextMenu(self, position: QPoint) -> None:
        self.contextMenu.exec(self.mapToGlobal(position))
    
    def setupContextMenu(self) -> None:
        menu = QMenu(self)
        QWidgetUtility.setMenuAttributes(menu)

        undoAction = QAction(parent = menu, text = "Отменить",
            icon = QResourceProvider.getIcon(QIcons.UNDO))
        undoAction.setShortcut(QKeySequence.StandardKey.Undo)
        undoAction.triggered.connect(self.binder.undoBinding.emit)
        self.binder.undoAvailableBinding.connect(undoAction.setEnabled)
        menu.undoAction = undoAction

        redoAction = QAction(parent = menu, text = "Повторить",
            icon = QResourceProvider.getIcon(QIcons.REDO))
        redoAction.setShortcut(QKeySequence.StandardKey.Redo)
        redoAction.triggered.connect(self.binder.redoBinding.emit)
        self.binder.redoAvailableBinding.connect(redoAction.setEnabled)
        menu.redoAction = redoAction

        cutAction = QAction(parent = menu, text = "Вырезать", 
            icon = QResourceProvider.getIcon(QIcons.CUT))
        cutAction.setShortcut(QKeySequence.StandardKey.Cut)
        cutAction.triggered.connect(self.binder.cutAvailableBinding.emit)
        self.binder.copyAvailableBinding.connect(cutAction.setEnabled)
        menu.cutAction = cutAction

        copyAction = QAction(parent = menu, text = "Копировать", 
            icon = QResourceProvider.getIcon(QIcons.COPY))
        copyAction.setShortcut(QKeySequence.StandardKey.Copy)
        copyAction.triggered.connect(self.binder.copyBinding.emit)
        self.binder.copyAvailableBinding.connect(copyAction.setEnabled)
        menu.copyAction = copyAction

        pasteAction = QAction(parent = menu, text = "Вставить", 
            icon = QResourceProvider.getIcon(QIcons.PASTE))
        pasteAction.setShortcut(QKeySequence.StandardKey.Paste)
        pasteAction.triggered.connect(self.binder.pasteBinding.emit)
        self.binder.pasteAvailableBinding.connect(pasteAction.setEnabled)
        menu.pasteAction = pasteAction

        menu.addSeparator()

        selectAllAction = QAction(parent = menu, text = "Выделить все",
            icon = QResourceProvider.getIcon(QIcons.COPY))
        selectAllAction.setShortcut(QKeySequence.StandardKey.SelectAll)
        selectAllAction.triggered.connect(self.binder.selectAllBinding.emit)
        menu.selectAllAction = selectAllAction

        menu.addActions((undoAction, redoAction))
        menu.addSeparator()
        menu.addActions((cutAction, copyAction, pasteAction))
        menu.addSeparator()
        menu.addAction(selectAllAction)

        self.contextMenu = menu