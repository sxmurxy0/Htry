from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QPushButton, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from widgets import Utility
from resources.Icons import *
from resources import ResourceProvider
from Binder import *

class QMenuPanel(QFrame):

    def __init__(self, parent: QWidget, binder: Binder) -> None:
        super().__init__(parent)
        
        self.setFixedHeight(40)
        self.setStyleSheet(ResourceProvider.loadStyleSheet("menu_panel"))
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.setLayout(layout)

        self.setupButtons(binder)
        self.setupFileMenu(binder)
        self.setupEditMenu(binder)
        
        Utility.addHorizontalSpacer(self)
    
    def setupButtons(self, binder: Binder) -> None:
        self.fileButton = QPushButton(parent = self, text = "Файл")
        self.layout().addWidget(self.fileButton)

        self.editButton = QPushButton(parent = self, text = "Изменить")
        self.layout().addWidget(self.editButton)

        Utility.addVerticalSeparator(widget = self, height = 22)

        self.saveButton = QPushButton(parent = self, 
            icon = ResourceProvider.getIcon(Icons.SAVE))
        self.saveButton.clicked.connect(binder.saveBinding.emit)
        self.saveButton.setToolTip("Сохранить")
        self.layout().addWidget(self.saveButton)

        Utility.addVerticalSeparator(widget = self, height = 22)

        self.undoButton = QPushButton(parent = self, 
            icon = ResourceProvider.getIcon(Icons.UNDO))
        self.undoButton.setShortcut(QKeySequence("Ctrl+Z"))
        self.undoButton.clicked.connect(binder.undoBinding.emit)
        binder.undoAvailableBinding.connect(self.undoButton.setEnabled)
        self.layout().addWidget(self.undoButton)

        self.redoButton = QPushButton(parent = self, 
            icon = ResourceProvider.getIcon(Icons.REDO))
        self.redoButton.setShortcut(QKeySequence("Ctrl+Y"))
        self.redoButton.clicked.connect(binder.redoBinding.emit)
        binder.redoAvailableBinding.connect(self.redoButton.setEnabled)
        self.layout().addWidget(self.redoButton)

    def setupFileMenu(self, binder: Binder) -> None:
        fileMenu = QMenu(self)
        Utility.setMenuAttributes(fileMenu)

        createAction = QAction(parent = fileMenu, text = "Создать", 
            icon = ResourceProvider.getIcon(Icons.FILE))
        createAction.setShortcut(QKeySequence("Ctrl+N"))
        createAction.triggered.connect(binder.createDocumentBinding.emit)
        fileMenu.createAction = createAction

        openAction = QAction(parent = fileMenu, text = "Открыть", 
            icon = ResourceProvider.getIcon(Icons.FOLDER))
        openAction.setShortcut(QKeySequence("Ctrl+O"))
        openAction.triggered.connect(binder.openDocumentBinding.emit)
        fileMenu.openAction = openAction

        saveAction = QAction(parent = fileMenu, text = "Сохранить", 
            icon = ResourceProvider.getIcon(Icons.SAVE))
        saveAction.setShortcut(QKeySequence("Ctrl+S"))
        saveAction.triggered.connect(binder.saveBinding.emit)
        fileMenu.saveAction = saveAction

        saveAsAction = QAction(parent = fileMenu, text = "Сохранить как", 
            icon = ResourceProvider.getIcon(Icons.SAVE_AS))
        saveAsAction.triggered.connect(binder.saveAsBinding.emit)
        fileMenu.saveAsAction = saveAsAction

        quitAction = QAction(parent = fileMenu, text = "Выйти", 
            icon = ResourceProvider.getIcon(Icons.CROSS))
        quitAction.setShortcut(QKeySequence("Ctrl+Q"))
        quitAction.triggered.connect(binder.quitBinding.emit) 
        fileMenu.quitAction = quitAction

        fileMenu.addActions((createAction, openAction, saveAction, saveAsAction))
        fileMenu.addSeparator()
        fileMenu.addAction(quitAction)

        self.fileButton.setMenu(fileMenu)
        self.fileMenu = fileMenu
    
    def setupEditMenu(self, binder: Binder) -> None:
        editMenu = QMenu(self)
        Utility.setMenuAttributes(editMenu)

        cutAction = QAction(parent = editMenu, text = "Вырезать", 
            icon = ResourceProvider.getIcon(Icons.SCISSORS))
        cutAction.setShortcut(QKeySequence("Ctrl+X"))
        cutAction.triggered.connect(binder.cutBinding.emit)
        binder.cutAvailableBinding.connect(cutAction.setEnabled)
        editMenu.cutAction = cutAction

        copyAction = QAction(parent = editMenu, text = "Копировать", 
            icon = ResourceProvider.getIcon(Icons.COPY))
        copyAction.setShortcut(QKeySequence("Ctrl+C"))
        copyAction.triggered.connect(binder.copyBinding.emit)
        binder.copyAvailableBinding.connect(copyAction.setEnabled)
        editMenu.copyAction = copyAction

        pasteAction = QAction(parent = editMenu, text = "Вставить", 
            icon = ResourceProvider.getIcon(Icons.PASTE))
        pasteAction.setShortcut(QKeySequence("Ctrl+V"))
        pasteAction.triggered.connect(binder.pasteBinding.emit)
        binder.pasteAvailableBinding.connect(pasteAction.setEnabled)
        editMenu.pasteAction = pasteAction

        editMenu.addActions((cutAction, copyAction, pasteAction))
        
        self.editButton.setMenu(editMenu)
        self.editMenu = editMenu