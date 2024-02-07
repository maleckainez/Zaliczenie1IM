from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap
import sys



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrintApp()
    sys.exit(app.exec())
