from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class Binder(QObject):

    create_document_binding = pyqtSignal()
    open_document_binding = pyqtSignal()

    save_binding = pyqtSignal()
    save_as_binding = pyqtSignal()

    close_binding = pyqtSignal()

    cut_binding = pyqtSignal()
    copy_binding = pyqtSignal()
    paste_binding = pyqtSignal()

    undo_binding = pyqtSignal()
    redo_binding = pyqtSignal()

    hotbar_font_binding = pyqtSignal(QFont)
    cursor_font_binding = pyqtSignal(QFont)

    hotbar_font_size_binding = pyqtSignal(int)
    cursor_font_size_binding = pyqtSignal(int)

    hotbar_bold_binding = pyqtSignal(bool)
    cursor_bold_binding = pyqtSignal(bool)

    hotbar_italic_binding = pyqtSignal(bool)
    cursor_italic_binding = pyqtSignal(bool)

    hotbar_underline_binding = pyqtSignal(bool)
    cursor_underline_binding = pyqtSignal(bool)

    hotbar_strikethrough_binding = pyqtSignal(bool)
    cursor_strikethrough_binding = pyqtSignal(bool)

    hotbar_text_color_binding = pyqtSignal(QColor)
    cursor_text_color_binding = pyqtSignal(QColor)

    hotbar_bg_color_binding = pyqtSignal(QColor)
    cursor_bg_color_binding = pyqtSignal(QColor)

    hotbar_alignment_binding = pyqtSignal(Qt.AlignmentFlag)
    cursor_alignment_binding = pyqtSignal(Qt.AlignmentFlag)

    insert_picture_binding = pyqtSignal()
    insert_link_bindng = pyqtSignal()