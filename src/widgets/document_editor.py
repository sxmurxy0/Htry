from PyQt6.QtWidgets import QWidget, QTextEdit, QScrollArea
from PyQt6.QtGui import QTextFrameFormat, QKeyEvent, QPaintEvent, QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import QSizeF, Qt
from binder import Binder

class QDocumentEditor(QTextEdit):

    PAGE_WIDTH = 780
    PAGE_HEIGHT = 1000
    PAGE_SIZE = QSizeF(PAGE_WIDTH, PAGE_HEIGHT)
    MARGIN = 50
    SPACING = 30

    def __init__(self, parent: QWidget, scroll_area: QScrollArea, binder: Binder):
        super().__init__(parent)

        self.scroll_area = scroll_area
        self.setFixedSize(QDocumentEditor.PAGE_WIDTH, QDocumentEditor.PAGE_HEIGHT)

        self.document().setPageSize(QDocumentEditor.PAGE_SIZE)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        frame_format = QTextFrameFormat()
        frame_format.setMargin(QDocumentEditor.MARGIN)
        frame_format.setBottomMargin(QDocumentEditor.MARGIN + QDocumentEditor.SPACING)

        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        brush.setColor(QColor("red"))
        frame_format.setBorder(1)
        frame_format.setBorderBrush(brush)

        self.document().rootFrame().setFrameFormat(frame_format)

        self.textChanged.connect(self.updateHeight)
        self.cursorPositionChanged.connect(self.updateCurrentScroll)
    
    def updateCurrentScroll(self):
        pos = self.mapToParent(self.cursorRect().center())
        self.scroll_area.ensureVisible(pos.x(), pos.y())
    
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
                QDocumentEditor.PAGE_WIDTH - 2, QDocumentEditor.PAGE_HEIGHT - QDocumentEditor.SPACING - 3)

        painter.restore()

        super().paintEvent(event)