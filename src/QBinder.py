from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from documents.QDocument import QDocument

class QBinder(QObject):

    createDocumentBinding = pyqtSignal()
    openDocumentBinding = pyqtSignal()

    saveDocumentBinding = pyqtSignal()
    saveDocumentAsBinding = pyqtSignal()

    quitBinding = pyqtSignal()

    cutBinding = pyqtSignal()
    cutAvailableBinding = pyqtSignal(bool)

    copyBinding = pyqtSignal()
    copyAvailableBinding = pyqtSignal(bool)

    pasteBinding = pyqtSignal()
    pasteAvailableBinding = pyqtSignal(bool)

    undoBinding = pyqtSignal()
    undoAvailableBinding = pyqtSignal(bool)

    redoBinding = pyqtSignal()
    redoAvailableBinding = pyqtSignal(bool)

    hotbarFontBinding = pyqtSignal(QFont)
    cursorFontBinding = pyqtSignal(QFont)

    hotbarFontSizeBinding = pyqtSignal(int)
    cursorFontSizeBinding = pyqtSignal(int)

    hotbarBoldBinding = pyqtSignal(bool)
    cursorBoldBinding = pyqtSignal(bool)

    hotbarItalicBinding = pyqtSignal(bool)
    cursorItalicBinding = pyqtSignal(bool)

    hotbarUnderlineBinding = pyqtSignal(bool)
    cursorUnderlineBinding = pyqtSignal(bool)

    hotbarStrikethroughBinding = pyqtSignal(bool)
    cursorStrikethroughBinding = pyqtSignal(bool)

    hotbarTextColorBinding = pyqtSignal(QColor)
    cursorTextColorBinding = pyqtSignal(QColor)

    hotbarBgColorBinding = pyqtSignal(QColor)
    cursorBgColorBinding = pyqtSignal(QColor)

    hotbarAlignmentBinding = pyqtSignal(Qt.AlignmentFlag)
    cursorAlignmentBinding = pyqtSignal(Qt.AlignmentFlag)

    insertPictureBinding = pyqtSignal()
    insertLinkBindng = pyqtSignal()

    documentUpdatedBinding = pyqtSignal(QDocument)