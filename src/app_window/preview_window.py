from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QMainWindow, QScrollArea


class PreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paddie - Preview")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)

        self.resize(800, 600)

    def set_image(self, pixmap_path):
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            self.image_label.setText("Failed to load preview image")
            return

        self.image_label.setPixmap(pixmap)
