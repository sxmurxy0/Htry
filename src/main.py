from PyQt6.QtWidgets import QApplication
from widgets.window import QWindow
from PyQt6.QtGui import QFontDatabase
import resources_provider
import sys, resources

if __name__ == "__main__":
    application = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont(":fonts/Malgun_Gothic.ttf")
    application.setStyleSheet(resources_provider.getStyleSheet("common"))

    window = QWindow()
    window.setup()
    window.showMaximized()

    sys.exit(application.exec())