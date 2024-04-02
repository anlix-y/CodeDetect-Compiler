import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PIL import ImageGrab
from app import FileDialogExample

class ScreenshotApp(QLabel):
    def __init__(self):
        super().__init__()

        # Создаем объект QRubberBand для выделения области экрана
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.hide()

        # Загружаем изображение экрана в QLabel
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(QApplication.desktop().winId())
        self.setPixmap(pixmap)

        # Устанавливаем курсор и события мыши для выделения области экрана
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.ex = ex

    def mousePressEvent(self, event):
        # Сохраняем координаты начала выделения области экрана
        self.origin = event.pos()
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

    def mouseMoveEvent(self, event):
        # Обновляем геометрию QRubberBand при перемещении мыши
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        # Получаем координаты выбранной области экрана
        rect = self.rubber_band.geometry()
        x = rect.x()
        y = rect.y()
        width = rect.width()
        height = rect.height()

        # Делаем скриншот выбранной области экрана
        screenshot = ImageGrab.grab((x, y, x + width, y + height))

        # Сохраняем скриншот в файл
        screenshot.save('temp/screenshot.png')
        file_path = str(os.getcwd()) + "/temp/screenshot.png"
        # Вызываем метод showDialogWithFile для экземпляра FileDialogExample
        self.ex.showDialogWithFile(file_path)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialogExample()
    screenshot_app = ScreenshotApp()
    screenshot_app.show()
    sys.exit(app.exec_())