from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import QLabel, QMainWindow


class PreviewWindow(QMainWindow):
    MAX_SCREEN_WIDTH_RATIO = 0.9
    MAX_SCREEN_HEIGHT_RATIO = 0.85

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paddie - Preview")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_label)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)

    def set_image(self, pixmap_path):
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            self.image_label.setText("Failed to load preview image")
            self.setFixedSize(360, 120)
            return

        display_size = self._fit_to_available_screen(pixmap.size())
        display_pixmap = pixmap.scaled(
            display_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.image_label.setPixmap(display_pixmap)
        self.image_label.setFixedSize(display_size)
        self.setFixedSize(display_size)

    def _fit_to_available_screen(self, image_size):
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return image_size

        available = screen.availableGeometry()
        max_size = QSize(
            max(1, int(available.width() * self.MAX_SCREEN_WIDTH_RATIO)),
            max(1, int(available.height() * self.MAX_SCREEN_HEIGHT_RATIO)),
        )

        if image_size.width() <= max_size.width() and image_size.height() <= max_size.height():
            return image_size

        return image_size.scaled(max_size, Qt.AspectRatioMode.KeepAspectRatio)
