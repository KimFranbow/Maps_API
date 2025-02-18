from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
import requests
import sys

API_KEY_STATIC = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'


class WinMap(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Maps")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.g_map = QLabel(self)
        layout.addWidget(self.g_map)

        self.map_zoom = 15
        self.map_ll = [44.486926, 33.396157]
        self.map_key = API_KEY_STATIC

        self.step_size = 0.01 / self.map_zoom * 5

        self.refresh_map()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_PageUp:
            self.map_zoom = min(self.map_zoom + 1, 18)
            if 1 <= self.map_zoom <= 3:
                self.step_size = 0.01 / self.map_zoom * 50
            elif 3 <=  self.map_zoom <= 5:
                self.step_size = 0.01 / self.map_zoom * 40
            elif 5 <= self.map_zoom <= 8:
                self.step_size = 0.01 / self.map_zoom * 30
            elif 8 <= self.map_zoom <= 10:
                self.step_size = 0.01 / self.map_zoom * 20
            elif 10 <= self.map_zoom <= 15:
                self.step_size = 0.01 / self.map_zoom * 10
            elif 15 <= self.map_zoom <= 18:
                self.step_size = 0.01 / self.map_zoom
        elif event.key() == Qt.Key.Key_PageDown:
            self.map_zoom = max(self.map_zoom - 1, 1)
            if 1 <= self.map_zoom <= 3:
                self.step_size = 0.01 / self.map_zoom * 50
            elif 3 <= self.map_zoom <= 5:
                self.step_size = 0.01 / self.map_zoom * 40
            elif 5 <= self.map_zoom <= 8:
                self.step_size = 0.01 / self.map_zoom * 30
            elif 8 <= self.map_zoom <= 10:
                self.step_size = 0.01 / self.map_zoom * 20
            elif 10 <= self.map_zoom <= 15:
                self.step_size = 0.01 / self.map_zoom * 10
            elif 15 <= self.map_zoom <= 18:
                self.step_size = 0.01 / self.map_zoom
        elif event.key() == Qt.Key.Key_Up:
            self.map_ll[1] += self.step_size
        elif event.key() == Qt.Key.Key_Down:
            self.map_ll[1] -= self.step_size
        elif event.key() == Qt.Key.Key_Left:
            self.map_ll[0] -= self.step_size
        elif event.key() == Qt.Key.Key_Right:
            self.map_ll[0] += self.step_size
        self.map_ll[0] = max(-180, min(180, self.map_ll[0]))
        self.map_ll[1] = max(-90, min(90, self.map_ll[1]))
        self.refresh_map()


    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'apikey': self.map_key,
        }

        response = requests.get('https://static-maps.yandex.ru/v1', params=map_params)

        if response.status_code == 200:
            img = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(img)

            self.g_map.setPixmap(pixmap)
        else:
            print("Ошибка при загрузке карты:", response.status_code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WinMap()
    main_window.show()
    sys.exit(app.exec())