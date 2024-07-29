from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFontDatabase
from widgets.Window import *
from resources import ResourceProvider
import sys

def setupEnvironment() -> None:
    QDir.addSearchPath("fonts", "assets/fonts/")
    QDir.addSearchPath("icons", "assets/icons/")
    QDir.addSearchPath("styles", "assets/styles/")

    QFontDatabase.addApplicationFont("fonts:Malgun.ttf")

if __name__ == "__main__":
    application = QApplication(sys.argv + ["-platform", "windows:darkmode=2", "-style", "windows"])
    setupEnvironment()
    application.setStyleSheet(ResourceProvider.loadStyleSheet("common"))
    
    window = QWindow()
    window.showMaximized()

    sys.exit(application.exec())