from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QPushButton, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from widgets import utility
from resources.icons import Icons
from resources import resource_provider
from binder import Binder

class QMenuPanel(QFrame):

    def __init__(self, parent: QWidget, binder: Binder) -> None:
        super().__init__(parent)
        
        self.setFixedHeight(40)
        self.setStyleSheet(resource_provider.getStyleSheet("menu_panel"))
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.setLayout(layout)

        self.setupButtons(binder)
        self.setupFileMenu(binder)
        self.setupEditMenu(binder)
        
        utility.addHorizontalSpacer(self)
    
    def setupButtons(self, binder: Binder) -> None:
        self.file_button = QPushButton(parent = self, text = "Файл")
        self.layout().addWidget(self.file_button)

        self.edit_button = QPushButton(parent = self, text = "Изменить")
        self.layout().addWidget(self.edit_button)

        utility.addVerticalSeparator(widget = self, height = 22)

        self.save_button = QPushButton(parent = self, 
            icon = resource_provider.getIcon(Icons.SAVE))
        self.save_button.clicked.connect(binder.save_binding.emit)
        self.save_button.setToolTip("Сохранить")
        self.layout().addWidget(self.save_button)

        utility.addVerticalSeparator(widget = self, height = 22)

        self.undo_button = QPushButton(parent = self, 
            icon = resource_provider.getIcon(Icons.UNDO))
        self.undo_button.setShortcut(QKeySequence("Ctrl+Z"))
        self.undo_button.clicked.connect(binder.undo_binding.emit)
        self.layout().addWidget(self.undo_button)

        self.redo_button = QPushButton(parent = self, 
            icon = resource_provider.getIcon(Icons.REDO))
        self.redo_button.setShortcut(QKeySequence("Ctrl+Y"))
        self.redo_button.clicked.connect(binder.redo_binding.emit)
        self.layout().addWidget(self.redo_button)

    def setupFileMenu(self, binder: Binder) -> None:
        file_menu = QMenu(self)
        
        utility.setMenuAttributes(file_menu)

        create_action = QAction(parent = file_menu, text = "Создать", 
            icon = resource_provider.getIcon(Icons.FILE))
        create_action.setShortcut(QKeySequence("Ctrl+N"))
        create_action.triggered.connect(binder.create_document_binding.emit)

        open_action = QAction(parent = file_menu, text = "Открыть", 
            icon = resource_provider.getIcon(Icons.FOLDER))
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(binder.open_document_binding.emit)

        save_action = QAction(parent = file_menu, text = "Сохранить", 
            icon = resource_provider.getIcon(Icons.SAVE))
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(binder.save_binding.emit)

        save_as_action = QAction(parent = file_menu, text = "Сохранить как", 
            icon = resource_provider.getIcon(Icons.SAVE_AS))
        save_as_action.triggered.connect(binder.save_as_binding.emit)

        close_action = QAction(parent = file_menu, text = "Выйти", 
            icon = resource_provider.getIcon(Icons.CROSS))
        close_action.setShortcut(QKeySequence("Ctrl+Q"))
        close_action.triggered.connect(binder.close_binding.emit) 

        file_menu.addActions((create_action, open_action, save_action, save_as_action))
        file_menu.addSeparator()
        file_menu.addAction(close_action)

        self.file_button.setMenu(file_menu)
    
    def setupEditMenu(self, binder: Binder) -> None:
        edit_menu = QMenu(self)
        utility.setMenuAttributes(edit_menu)

        cut_action = QAction(parent = edit_menu, text = "Вырезать", 
            icon = resource_provider.getIcon(Icons.SCISSORS))
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        cut_action.triggered.connect(binder.cut_binding)

        copy_action = QAction(parent = edit_menu, text = "Копировать", 
            icon = resource_provider.getIcon(Icons.COPY))
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(binder.copy_binding.emit)

        paste_action = QAction(parent = edit_menu, text = "Вставить", 
            icon = resource_provider.getIcon(Icons.PASTE))
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(binder.paste_binding.emit)

        edit_menu.addActions((cut_action, copy_action, paste_action))

        self.edit_button.setMenu(edit_menu)