import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow


app = QApplication(sys.argv)
ui = MainWindow()
ui.show()
sys.exit(app.exec())