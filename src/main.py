from PyQt6.QtWidgets import QApplication
from widgets.window import QWindow
from PyQt6.QtGui import QFontDatabase
from resources import resource_provider
import sys, resources.data

if __name__ == "__main__":
    application = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont(":fonts/Malgun_Gothic.ttf")
    application.setStyleSheet(resource_provider.getStyleSheet("common"))

    window = QWindow()
    window.setup()
    window.showMaximized()

    sys.exit(application.exec())