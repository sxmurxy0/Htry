from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QPushButton, QMenu
from PyQt6.QtGui import QIcon, QAction, QKeySequence
from widgets.QWidgetUtility import QWidgetUtility
from resources.QIcons import QIcons
from resources.QResourceProvider import QResourceProvider
from QBinder import QBinder

class QMenuPanel(QFrame):

    class QMenuPanelButton(QPushButton):

        def __init__(self, parent: QWidget = None, text: str = None, icon: QIcon = None) -> None:
            super().__init__(parent = parent, text = text)
            if icon:
                self.setIcon(icon)

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
        self.fileButton = QMenuPanel.QMenuPanelButton(parent = self, text = "Файл")
        self.layout().addWidget(self.fileButton)

        self.editButton = QMenuPanel.QMenuPanelButton(parent = self, text = "Изменить")
        self.layout().addWidget(self.editButton)

        QWidgetUtility.addVerticalSeparator(widget = self, height = 22)

        self.saveButton = QMenuPanel.QMenuPanelButton(parent = self, 
            icon = QResourceProvider.getIcon(QIcons.SAVE))
        self.saveButton.clicked.connect(binder.saveDocumentBinding.emit)
        self.layout().addWidget(self.saveButton)

        QWidgetUtility.addVerticalSeparator(widget = self, height = 22)

        self.undoButton = QMenuPanel.QMenuPanelButton(parent = self, 
            icon = QResourceProvider.getIcon(QIcons.UNDO))
        self.undoButton.clicked.connect(binder.undoBinding.emit)
        binder.undoAvailableBinding.connect(self.undoButton.setEnabled)
        self.layout().addWidget(self.undoButton)

        self.redoButton = QMenuPanel.QMenuPanelButton(parent = self, 
            icon = QResourceProvider.getIcon(QIcons.REDO))
        self.redoButton.clicked.connect(binder.redoBinding.emit)
        binder.redoAvailableBinding.connect(self.redoButton.setEnabled)
        self.layout().addWidget(self.redoButton)

    def setupFileMenu(self, binder: QBinder) -> None:
        fileMenu = QMenu(self)
        QWidgetUtility.setMenuAttributes(fileMenu)

        createAction = QAction(parent = fileMenu, text = "Создать", 
            icon = QResourceProvider.getIcon(QIcons.FILE))
        createAction.setShortcut(QKeySequence.StandardKey.New)
        createAction.triggered.connect(binder.createDocumentBinding.emit)
        fileMenu.createAction = createAction

        openAction = QAction(parent = fileMenu, text = "Открыть", 
            icon = QResourceProvider.getIcon(QIcons.FOLDER))
        openAction.setShortcut(QKeySequence.StandardKey.Open)
        openAction.triggered.connect(binder.openDocumentBinding.emit)
        fileMenu.openAction = openAction

        saveAction = QAction(parent = fileMenu, text = "Сохранить", 
            icon = QResourceProvider.getIcon(QIcons.SAVE))
        saveAction.setShortcut(QKeySequence.StandardKey.Save)
        saveAction.triggered.connect(binder.saveDocumentBinding.emit)
        fileMenu.saveAction = saveAction

        saveAsAction = QAction(parent = fileMenu, text = "Сохранить как", 
            icon = QResourceProvider.getIcon(QIcons.SAVE_AS))
        saveAsAction.setShortcut(QKeySequence.StandardKey.SaveAs)
        saveAsAction.triggered.connect(binder.saveDocumentAsBinding.emit)
        fileMenu.saveAsAction = saveAsAction

        quitAction = QAction(parent = fileMenu, text = "Выйти", 
            icon = QResourceProvider.getIcon(QIcons.CROSS))
        quitAction.setShortcut(QKeySequence.StandardKey.Close)
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
            icon = QResourceProvider.getIcon(QIcons.CUT))
        cutAction.setShortcut(QKeySequence.StandardKey.Cut)
        cutAction.triggered.connect(binder.cutBinding.emit)
        binder.cutAvailableBinding.connect(cutAction.setEnabled)
        editMenu.cutAction = cutAction

        copyAction = QAction(parent = editMenu, text = "Копировать", 
            icon = QResourceProvider.getIcon(QIcons.COPY))
        copyAction.setShortcut(QKeySequence.StandardKey.Copy)
        copyAction.triggered.connect(binder.copyBinding.emit)
        binder.copyAvailableBinding.connect(copyAction.setEnabled)
        editMenu.copyAction = copyAction

        pasteAction = QAction(parent = editMenu, text = "Вставить", 
            icon = QResourceProvider.getIcon(QIcons.PASTE))
        pasteAction.setShortcut(QKeySequence.StandardKey.Paste)
        pasteAction.triggered.connect(binder.pasteBinding.emit)
        binder.pasteAvailableBinding.connect(pasteAction.setEnabled)
        editMenu.pasteAction = pasteAction

        editMenu.addActions((cutAction, copyAction, pasteAction))
        
        self.editButton.setMenu(editMenu)
        self.editMenu = editMenu