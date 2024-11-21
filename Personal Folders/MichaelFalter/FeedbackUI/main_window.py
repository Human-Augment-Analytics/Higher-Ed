import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from template_dialog import TemplateDialog
from parse_dialog import ParseDialog
import os

# Add the root project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feedback Template Manager")

        # Layout
        layout = QVBoxLayout()
        generate_btn = QPushButton("Generate Template")
        parse_btn = QPushButton("Parse Template")

        # Connect buttons to their respective dialogs
        generate_btn.clicked.connect(self.open_generate_dialog)
        parse_btn.clicked.connect(self.open_parse_dialog)

        layout.addWidget(generate_btn)
        layout.addWidget(parse_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_generate_dialog(self):
        dialog = TemplateDialog(self)
        dialog.exec_()

    def open_parse_dialog(self):
        dialog = ParseDialog(self)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
