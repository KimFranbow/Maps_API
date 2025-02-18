import sys
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
import requests

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
