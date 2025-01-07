from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image, ImageDraw


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pillow Script Runner")

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText(
            "Write your Pillow code here.\n"
            "Example:\n"
            "image = Image.new('RGB', (400, 300), 'white')\n"
            "draw = ImageDraw.Draw(image)\n"
            "draw.rectangle([50, 50, 200, 150], fill='blue')\n"
            "draw.ellipse([100, 100, 300, 250], fill='red')\n"
            "draw.text((10, 10), 'Hello Pillow!', fill='black')"
        )
        left_layout.addWidget(self.text_editor)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_code)
        left_layout.addWidget(run_button)

        splitter.addWidget(left_widget)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #000000;")
        splitter.addWidget(self.image_label)

        splitter.setSizes([400, 400])

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(splitter)

        self.setCentralWidget(central_widget)

    def run_code(self):
        code = self.text_editor.toPlainText()
        try:
            local_context = {"Image": Image, "ImageDraw": ImageDraw}
            exec(code, {}, local_context)

            image = local_context.get("image")
            if image is None or not isinstance(image, Image.Image):
                raise ValueError("Your script must create an image object named 'image'.")

            qt_image = self.pillow_to_qt_image(image)
            self.image_label.setPixmap(QPixmap.fromImage(qt_image))

        except Exception as e:
            self.image_label.setText(f"Error:\n{e}")

    def pillow_to_qt_image(self, pillow_image):
        """
        Convert a Pillow image to a Qt-compatible QImage.
        """
        pillow_image = pillow_image.convert("RGBA")
        data = pillow_image.tobytes("raw", "RGBA")
        qimage = QImage(data, pillow_image.width, pillow_image.height, QImage.Format_RGBA8888)
        return qimage


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

