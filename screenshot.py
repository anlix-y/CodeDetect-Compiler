import os
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PIL import ImageGrab
from front import FileDialogExample

class ScreenshotApp(QLabel):
    def __init__(self):
        super().__init__()

        # Создаем объект QRubberBand для выделения области экрана
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.hide()

        # Получаем геометрию всего экрана, включая все мониторы
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry()

        # Создаем QPixmap нужного размера
        pixmap = QPixmap(screen_geometry.size())

        # Делаем скриншот всего экрана
        pixmap = QApplication.primaryScreen().grabWindow(desktop.winId())

        # Загружаем скриншот в QLabel
        self.setPixmap(pixmap)

        # Устанавливаем курсор и события мыши для выделения области экрана
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.ex = ex

        # Открываем предпросмотр для выделения области во весь экран
        self.showFullScreen()

    def mousePressEvent(self, event):
        # Сохраняем координаты начала выделения области экрана
        self.origin = event.pos()
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

    def mouseMoveEvent(self, event):
        # Обновляем геометрию QRubberBand при перемещении мыши
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        # Создаем новый QPixmap с выделенной областью
        rect = self.rubber_band.geometry()
        selected_area = self.pixmap().copy(rect)

        # Сохраняем готовый скриншот в файл
        selected_area.save('temp/screenshot.png')
        file_path = str(os.getcwd()) + "/temp/screenshot.png"
        # Вызываем метод showDialogWithFile для экземпляра FileDialogExample
        self.ex.showDialogWithFile(file_path)
        self.close()

        # Скрываем выделитель
        self.rubber_band.hide()

class StartAppS():
    def __init__(self):
        app = QApplication(sys.argv)
        global ex
        ex = FileDialogExample()
        screenshot_app = ScreenshotApp()
        screenshot_app.show()
        app.exec_()

if __name__ == '__main__':
    StartAppS()