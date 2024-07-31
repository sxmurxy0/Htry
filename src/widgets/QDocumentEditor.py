from PyQt6.QtWidgets import QWidget, QTextEdit, QMenu
from PyQt6.QtGui import (QTextFrameFormat, QTextImageFormat, QKeyEvent, QPaintEvent, 
    QPainter, QPen, QBrush, QColor, QAction, QKeySequence, QFont)
from PyQt6.QtCore import Qt, QSizeF, QPoint
from widgets.QWidgetUtility import QWidgetUtility
from resources.Icons import Icons
from resources.QResourceProvider import QResourceProvider
from documents.QDocument import QDocument
from QBinder import QBinder

class QDocumentEditor(QTextEdit):

    PAGE_WIDTH = 780
    PAGE_HEIGHT = 980
    PAGE_SIZE = QSizeF(PAGE_WIDTH, PAGE_HEIGHT)
    PAGE_MARGIN = 50
    PAGE_SPACING = 30

    def __init__(self, parent: QWidget, binder: QBinder) -> None:
        super().__init__(parent)

        self.setFixedWidth(QDocumentEditor.PAGE_WIDTH)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setupContextMenu()
        self.customContextMenuRequested.connect(self.openContextMenu)

        binder.undoBinding.connect(self.undo)
        binder.redoBinding.connect(self.redo)
        binder.cutBinding.connect(self.cut)
        binder.copyBinding.connect(self.copy)
        binder.pasteBinding.connect(self.paste)

        binder.hotbarFontBinding.connect(self.setCurrentFont)
        binder.hotbarFontSizeBinding.connect(self.setFontPointSize)

        binder.hotbarBoldBinding.connect(lambda state: 
            self.setFontWeight(QFont.Weight.Bold if state else QFont.Weight.Normal))
        binder.hotbarItalicBinding.connect(self.setFontItalic)
        binder.hotbarUnderlineBinding.connect(self.setFontUnderline)
        binder.hotbarStrikethroughBinding.connect(self.setFontStrikethrough)

        binder.hotbarAlignmentBinding.connect(self.setAlignment)

        binder.documentUpdatedBinding.connect(self.setDocument)

        self.undoAvailable.connect(binder.undoAvailableBinding.emit)
        self.redoAvailable.connect(binder.redoAvailableBinding.emit)
        self.copyAvailable.connect(binder.cutAvailableBinding.emit)
        self.copyAvailable.connect(binder.copyAvailableBinding.emit)

        self.textChanged.connect(self.updateBounds)
        self.currentCharFormatChanged.connect(self.updateHotbarState)

        self.binder = binder
    
    def setFontStrikethrough(self, state: bool) -> None:
        font = self.currentFont()
        font.setStrikeOut(state)
        self.setCurrentFont(font)
    
    def updateHotbarState(self) -> None:
        self.blockSignals(True)

        self.binder.cursorFontBinding.emit(self.currentFont())
        self.binder.cursorFontSizeBinding.emit(int(self.fontPointSize()))

        self.binder.cursorBoldBinding.emit(
                True if self.currentFont().weight() == QFont.Weight.Bold else False)
        self.binder.cursorItalicBinding.emit(self.fontItalic())
        self.binder.cursorUnderlineBinding.emit(self.fontUnderline())
        self.binder.cursorStrikethroughBinding.emit(self.currentFont().strikeOut())

        self.binder.cursorAlignmentBinding.emit(self.alignment())

        self.blockSignals(False)
    
    def setDocument(self, document: QDocument) -> None:
        super().setDocument(document)

        self.updateBounds()

        format = QTextFrameFormat()
        format.setMargin(QDocumentEditor.PAGE_MARGIN)
        format.setBottomMargin(QDocumentEditor.PAGE_MARGIN + QDocumentEditor.PAGE_SPACING)

        format.setBorder(1)
        format.setBorderBrush(QBrush(QColor("green"), Qt.BrushStyle.SolidPattern))

        self.document().rootFrame().setFrameFormat(format)
    
    def updateBounds(self):
        self.document().setPageSize(QDocumentEditor.PAGE_SIZE)
        self.setFixedHeight(self.document().pageCount() * QDocumentEditor.PAGE_HEIGHT)
        
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self.viewport())
        painter.setPen(QPen(QColor("#e6e3ed"), 1))
        painter.setBrush(QBrush(QColor("white"), Qt.BrushStyle.SolidPattern))
        
        for i in range(self.document().pageCount()):
            painter.drawRect(1, i * (QDocumentEditor.PAGE_HEIGHT) + 2,
                QDocumentEditor.PAGE_WIDTH - 2, QDocumentEditor.PAGE_HEIGHT - QDocumentEditor.PAGE_SPACING  - 3)

        super().paintEvent(event)
    
    def openContextMenu(self, position: QPoint) -> None:
        self.contextMenu.exec(self.mapToGlobal(position))
    
    def setupContextMenu(self) -> None:
        menu = QMenu(self)
        QWidgetUtility.setMenuAttributes(menu)

        undoAction = QAction(parent = menu, text = "Отменить",
            icon = QResourceProvider.getIcon(Icons.UNDO))
        undoAction.setShortcut(QKeySequence("Ctrl+Z"))
        undoAction.triggered.connect(self.undo)
        self.undoAvailable.connect(undoAction.setEnabled)
        menu.undoAction = undoAction

        redoAction = QAction(parent = menu, text = "Повторить",
            icon = QResourceProvider.getIcon(Icons.REDO))
        redoAction.setShortcut(QKeySequence("Ctrl+Y"))
        redoAction.triggered.connect(self.redo)
        self.redoAvailable.connect(redoAction.setEnabled)
        menu.redoAction = redoAction

        cutAction = QAction(parent = menu, text = "Вырезать", 
            icon = QResourceProvider.getIcon(Icons.CUT))
        cutAction.setShortcut(QKeySequence("Ctrl+X"))
        cutAction.triggered.connect(self.cut)
        self.copyAvailable.connect(cutAction.setEnabled)
        menu.cutAction = cutAction

        copyAction = QAction(parent = menu, text = "Копировать", 
            icon = QResourceProvider.getIcon(Icons.COPY))
        copyAction.setShortcut(QKeySequence("Ctrl+C"))
        copyAction.triggered.connect(self.copy)
        self.copyAvailable.connect(copyAction.setEnabled)
        menu.copyAction = copyAction

        pasteAction = QAction(parent = menu, text = "Вставить", 
            icon = QResourceProvider.getIcon(Icons.PASTE))
        pasteAction.setShortcut(QKeySequence("Ctrl+V"))
        pasteAction.triggered.connect(self.paste)
        menu.pasteAction = pasteAction

        menu.addSeparator()

        selectAllAction = QAction(parent = menu, text = "Выделить все", 
            icon = QResourceProvider.getIcon(Icons.COPY))
        selectAllAction.setShortcut(QKeySequence("Ctrl+A"))
        selectAllAction.triggered.connect(self.selectAll)
        menu.selectAllAction = selectAllAction

        menu.addActions((undoAction, redoAction))
        menu.addSeparator()
        menu.addActions((cutAction, copyAction, pasteAction))
        menu.addSeparator()
        menu.addAction(selectAllAction)

        self.contextMenu = menu