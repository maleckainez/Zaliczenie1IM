from PyQt6.QtCore import QObject, QThread, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

class PngPrinter(QObject):
    finished = pyqtSignal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def print_png(self):
        app = QApplication.instance()
        printer = QPrinter()
        if printer.setup(app.activeWindow()):
            image = QImage(self.filename)
            painter = QPainter(printer)
            painter.drawImage(QRectF(0, 0, image.width(), image.height()), image)
            painter.end()
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.png_printer = PngPrinter('my_image.png')
        self.png_printer.finished.connect(self.printing_finished)
        self.thread = QThread()  # Move thread initialization to __init__

    def printing_finished(self):
        print("Printing finished")

    def print_png(self):
        self.png_printer.moveToThread(self.thread)
        self.thread.started.connect(self.png_printer.print_png)
        self.png_printer.finished.connect(self.thread.quit)
        self.thread.start()

    def __del__(self):
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.print_png()
    window.show()
    sys.exit(app.exec())
