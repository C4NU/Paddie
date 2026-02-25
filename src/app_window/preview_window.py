from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class PreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paddie - Preview")
        
        # Scroll area to handle large images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)
        
        self.resize(800, 600)

    def retranslateUi(self, widget):
        self.setWindowTitle(self.tr("Paddie - Preview"))

    def set_image(self, pixmap_path):
        pixmap = QPixmap(pixmap_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            # Adjust window size to image size if it's smaller than reasonable limit
            # but keep it within some bounds
            img_width = pixmap.width()
            img_height = pixmap.height()
            
            # Optional: auto-resize window to fit image (with limits)
            # self.resize(min(img_width + 20, 1200), min(img_height + 20, 900))
        else:
            self.image_label.setText("Failed to load preview image")
