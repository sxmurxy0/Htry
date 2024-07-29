from PyQt6.QtWidgets import QWidget, QTextEdit, QScrollArea, QHBoxLayout, QMenu
from PyQt6.QtGui import (QTextFrameFormat, QKeyEvent, QPaintEvent, QPainter, 
    QPen, QBrush, QColor, QAction, QKeySequence)
from PyQt6.QtCore import QSizeF, QPoint, Qt
from widgets import Utility
from resources.Icons import *
from resources import ResourceProvider
from Binder import *

class QDocumentEditor(QScrollArea):

    PAGE_WIDTH = 780
    PAGE_HEIGHT = 1000
    PAGE_SIZE = QSizeF(PAGE_WIDTH, PAGE_HEIGHT)
    PAGE_MARGIN = 50
    PAGE_SPACING = 30

    class QPageEdit(QTextEdit):

        def __init__(self, parent: QWidget, binder: Binder):
            super().__init__(parent)

            self.setFixedSize(QDocumentEditor.PAGE_WIDTH, QDocumentEditor.PAGE_HEIGHT)
            self.document().setPageSize(QDocumentEditor.PAGE_SIZE)

            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            frameFormat = QTextFrameFormat()
            frameFormat.setMargin(QDocumentEditor.PAGE_MARGIN)
            frameFormat.setBottomMargin(QDocumentEditor.PAGE_MARGIN + QDocumentEditor.PAGE_SPACING)

            brush = QBrush()
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            brush.setColor(QColor("red"))
            frameFormat.setBorder(1)
            frameFormat.setBorderBrush(brush)

            self.document().rootFrame().setFrameFormat(frameFormat)

            self.textChanged.connect(self.updateHeight)

            self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self.createContextMenu)
        
        def updateHeight(self):
            self.setFixedHeight(self.document().pageCount() * QDocumentEditor.PAGE_HEIGHT)

        def keyReleaseEvent(self, event: QKeyEvent):
            if event.key() == Qt.Key.Key_Return:
                self.document().setPageSize(QDocumentEditor.PAGE_SIZE)
            
        def paintEvent(self, event: QPaintEvent):
            painter = QPainter(self.viewport())
            pen = QPen()
            pen.setColor(QColor("#e6e3ed"))
            pen.setWidth(1)
            painter.setPen(pen)
            brush = QBrush()
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            brush.setColor(QColor("white"))
            painter.setBrush(brush)
            painter.save()
            
            for i in range(self.document().pageCount()):
                painter.drawRect(1, i * (QDocumentEditor.PAGE_HEIGHT) + 2,
                    QDocumentEditor.PAGE_WIDTH - 2, QDocumentEditor.PAGE_HEIGHT - QDocumentEditor.PAGE_SPACING  - 3)

            painter.restore()

            super().paintEvent(event)
        
        def createContextMenu(self, position: QPoint) -> None:
            menu = QMenu(self)
            Utility.setMenuAttributes(menu)

            undoAction = QAction(parent = menu, text = "Отменить",
                icon = ResourceProvider.getIcon(Icons.UNDO))
            undoAction.setShortcut(QKeySequence("Ctrl+Z"))

            redoAction = QAction(parent = menu, text = "Повторить",
                icon = ResourceProvider.getIcon(Icons.REDO))
            redoAction.setShortcut(QKeySequence("Ctrl+Y"))

            cutAction = QAction(parent = menu, text = "Вырезать", 
                icon = ResourceProvider.getIcon(Icons.SCISSORS))
            cutAction.setShortcut(QKeySequence("Ctrl+X"))

            copyAction = QAction(parent = menu, text = "Копировать", 
                icon = ResourceProvider.getIcon(Icons.COPY))
            copyAction.setShortcut(QKeySequence("Ctrl+C"))

            pasteAction = QAction(parent = menu, text = "Вставить", 
                icon = ResourceProvider.getIcon(Icons.PASTE))
            pasteAction.setShortcut(QKeySequence("Ctrl+V"))

            menu.addSeparator()

            selectAllAction = QAction(parent = menu, text = "Выделить все", 
                icon = ResourceProvider.getIcon(Icons.COPY))
            selectAllAction.setShortcut(QKeySequence("Ctrl+A"))

            menu.addActions((undoAction, redoAction))
            menu.addSeparator()
            menu.addActions((cutAction, copyAction, pasteAction))
            menu.addSeparator()
            menu.addAction(selectAllAction)

            menu.exec(self.mapToGlobal(position))
    
    def __init__(self, parent: QWidget, binder: Binder):
        super().__init__(parent)

        self.content = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 60, 0, 10)
        self.content.setLayout(layout)

        self.setWidget(self.content)
        self.setWidgetResizable(True)

        self.pageEdit = QDocumentEditor.QPageEdit(parent = self.content, binder = binder)
        self.content.layout().addWidget(self.pageEdit)

        self.pageEdit.cursorPositionChanged.connect(self.ensureCursorVisible)

    def ensureCursorVisible(self):
        position = self.pageEdit.mapToParent(self.pageEdit.cursorRect().center())
        self.ensureVisible(position.x(), position.y())