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

    selectAllBinding = pyqtSignal()

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

    hotbarStrikeoutBinding = pyqtSignal(bool)
    cursorStrikeoutBinding = pyqtSignal(bool)

    textColorBinding = pyqtSignal(QColor)
    bgColorBinding = pyqtSignal(QColor)

    hotbarAlignmentBinding = pyqtSignal(Qt.AlignmentFlag)
    cursorAlignmentBinding = pyqtSignal(Qt.AlignmentFlag)

    insertImageBinding = pyqtSignal()
    insertLinkBindng = pyqtSignal()

    hotbarIndentationBinding = pyqtSignal(int)
    cursorIndentationBinding = pyqtSignal(int)

    hotbarSpacingBinding = pyqtSignal(int)
    cursorSpacingBinding = pyqtSignal(int)

    resetFormatBinding = pyqtSignal()

    documentUpdatedBinding = pyqtSignal(QDocument)