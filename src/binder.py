from PyQt6.QtCore import QObject, pyqtSignal

class Binder(QObject):

    create_binding = pyqtSignal()
    open_binding = pyqtSignal()
    save_binding = pyqtSignal()
    save_as_binding = pyqtSignal()

    close_binding = pyqtSignal()

    cut_binding = pyqtSignal()
    copy_binding = pyqtSignal()
    paste_binding = pyqtSignal()

    undo_binding = pyqtSignal()
    redo_binding = pyqtSignal()

    hotbar_font_size_binding = pyqtSignal(int)
    cursor_font_size_binding = pyqtSignal(int)

    hotbar_bold_binding = pyqtSignal(bool)
    cursor_bold_binding = pyqtSignal(bool)

    hotbar_italic_binding = pyqtSignal(bool)
    cursor_italic_binding = pyqtSignal(bool)

    hotbar_underlined_binding = pyqtSignal(bool)
    cursor_underlined_binding = pyqtSignal(bool)

    hotbar_strikethrough_binding = pyqtSignal(bool)
    cursor_strikethrough_binding = pyqtSignal(bool)