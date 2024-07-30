from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QPushButton, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from widgets import QWidgetUtility
from core.resources.Icons import Icons
from core.resources import QResourceProvider
from core.QBinder import QBinder

class QMenuPanel(QFrame):

    def __init__(self, parent: QWidget, binder: QBinder) -> None:
        super().__init__(parent)
        
        self.setFixedHeight(40)
        self.setStyleSheet(QResourceProvider.getStyleSheet("menu_panel"))
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        self.setLayout(layout)

        self.setupButtons(binder)
        self.setupFileMenu(binder)
        self.setupEditMenu(binder)
        
        QWidgetUtility.addHorizontalSpacer(self)
    
    def setupButtons(self, binder: QBinder) -> None:
        self.fileButton = QPushButton(parent = self, text = "Файл")
        self.layout().addWidget(self.fileButton)

        self.editButton = QPushButton(parent = self, text = "Изменить")
        self.layout().addWidget(self.editButton)

        QWidgetUtility.addVerticalSeparator(widget = self, height = 22)

        self.saveButton = QPushButton(parent = self, 
            icon = QResourceProvider.getIcon(Icons.SAVE))
        self.saveButton.clicked.connect(binder.saveDocumentBinding.emit)
        self.saveButton.setToolTip("Сохранить")
        self.layout().addWidget(self.saveButton)

        QWidgetUtility.addVerticalSeparator(widget = self, height = 22)

        self.undoButton = QPushButton(parent = self, 
            icon = QResourceProvider.getIcon(Icons.UNDO))
        self.undoButton.setShortcut(QKeySequence("Ctrl+Z"))
        self.undoButton.clicked.connect(binder.undoBinding.emit)
        binder.undoAvailableBinding.connect(self.undoButton.setEnabled)
        self.layout().addWidget(self.undoButton)

        self.redoButton = QPushButton(parent = self, 
            icon = QResourceProvider.getIcon(Icons.REDO))
        self.redoButton.setShortcut(QKeySequence("Ctrl+Y"))
        self.redoButton.clicked.connect(binder.redoBinding.emit)
        binder.redoAvailableBinding.connect(self.redoButton.setEnabled)
        self.layout().addWidget(self.redoButton)

    def setupFileMenu(self, binder: QBinder) -> None:
        fileMenu = QMenu(self)
        QWidgetUtility.setMenuAttributes(fileMenu)

        createAction = QAction(parent = fileMenu, text = "Создать", 
            icon = QResourceProvider.getIcon(Icons.FILE))
        createAction.setShortcut(QKeySequence("Ctrl+N"))
        createAction.triggered.connect(binder.createDocumentBinding.emit)
        fileMenu.createAction = createAction

        openAction = QAction(parent = fileMenu, text = "Открыть", 
            icon = QResourceProvider.getIcon(Icons.FOLDER))
        openAction.setShortcut(QKeySequence("Ctrl+O"))
        openAction.triggered.connect(binder.openDocumentBinding.emit)
        fileMenu.openAction = openAction

        saveAction = QAction(parent = fileMenu, text = "Сохранить", 
            icon = QResourceProvider.getIcon(Icons.SAVE))
        saveAction.setShortcut(QKeySequence("Ctrl+S"))
        saveAction.triggered.connect(binder.saveDocumentBinding.emit)
        fileMenu.saveAction = saveAction

        saveAsAction = QAction(parent = fileMenu, text = "Сохранить как", 
            icon = QResourceProvider.getIcon(Icons.SAVE_AS))
        saveAsAction.triggered.connect(binder.saveDocumentAsBinding.emit)
        fileMenu.saveAsAction = saveAsAction

        quitAction = QAction(parent = fileMenu, text = "Выйти", 
            icon = QResourceProvider.getIcon(Icons.CROSS))
        quitAction.setShortcut(QKeySequence("Ctrl+Q"))
        quitAction.triggered.connect(binder.quitBinding.emit) 
        fileMenu.quitAction = quitAction

        fileMenu.addActions((createAction, openAction, saveAction, saveAsAction))
        fileMenu.addSeparator()
        fileMenu.addAction(quitAction)

        self.fileButton.setMenu(fileMenu)
        self.fileMenu = fileMenu
    
    def setupEditMenu(self, binder: QBinder) -> None:
        editMenu = QMenu(self)
        QWidgetUtility.setMenuAttributes(editMenu)

        cutAction = QAction(parent = editMenu, text = "Вырезать", 
            icon = QResourceProvider.getIcon(Icons.SCISSORS))
        cutAction.setShortcut(QKeySequence("Ctrl+X"))
        cutAction.triggered.connect(binder.cutBinding.emit)
        binder.cutAvailableBinding.connect(cutAction.setEnabled)
        editMenu.cutAction = cutAction

        copyAction = QAction(parent = editMenu, text = "Копировать", 
            icon = QResourceProvider.getIcon(Icons.COPY))
        copyAction.setShortcut(QKeySequence("Ctrl+C"))
        copyAction.triggered.connect(binder.copyBinding.emit)
        binder.copyAvailableBinding.connect(copyAction.setEnabled)
        editMenu.copyAction = copyAction

        pasteAction = QAction(parent = editMenu, text = "Вставить", 
            icon = QResourceProvider.getIcon(Icons.PASTE))
        pasteAction.setShortcut(QKeySequence("Ctrl+V"))
        pasteAction.triggered.connect(binder.pasteBinding.emit)
        binder.pasteAvailableBinding.connect(pasteAction.setEnabled)
        editMenu.pasteAction = pasteAction

        editMenu.addActions((cutAction, copyAction, pasteAction))
        
        self.editButton.setMenu(editMenu)
        self.editMenu = editMenu