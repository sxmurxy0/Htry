from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFontDatabase
from core.resources import QResourceProvider
from widgets.QWindow import QWindow
import sys

def setupEnvironment() -> None:
    QDir.addSearchPath("fonts", "assets/fonts/")
    QDir.addSearchPath("icons", "assets/icons/")
    QDir.addSearchPath("styles", "assets/styles/")

if __name__ == "__main__":
    setupEnvironment()
    
    application = QApplication(sys.argv + ["-platform", "windows:darkmode=2", "-style", "windows"])
    application.setStyleSheet(QResourceProvider.getStyleSheet("common"))
    QFontDatabase.addApplicationFont("fonts:Malgun_Gothic.ttf")
    
    window = QWindow()
    window.showMaximized()

    sys.exit(application.exec())