import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Simple App")
        self.setGeometry(100, 100, 300, 200)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)


        self.label = QLabel("Hello, PyQt6!", self)
        self.button = QPushButton("Click Me", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_click)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Button clicked!")
        self.hide()


app = QApplication(sys.argv)

# Create and show the main window
window = SimpleApp()
window.show()

# Run the app
sys.exit(app.exec())
