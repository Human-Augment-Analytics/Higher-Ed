import sys
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QComboBox,
    QFormLayout,
    QSpinBox,
    QApplication,
)
from PyQt5.QtCore import Qt
from template_generator import TemplateGenerator


class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Feedback Template")
        self.setMinimumSize(400, 400)

        # Store categories and metrics
        self.categories = {
            "Clarity and Presentation Metrics": ["Grammar", "Formatting"],
            "Content Understanding Metrics": ["Comprehension", "Accuracy"],
        }

        # Default filename
        self.default_filename = "feedback_template.docx"

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Reviewer and researcher details section
        details_layout = QFormLayout()
        self.reviewer_name_input = QLineEdit()
        self.group_name_input = QLineEdit()
        self.researcher_name_input = QLineEdit()
        details_layout.addRow("Reviewer Name:", self.reviewer_name_input)
        details_layout.addRow("Group Name:", self.group_name_input)
        details_layout.addRow("Researcher Name:", self.researcher_name_input)
        layout.addLayout(details_layout)

        # Category and Metric section
        self.categories_layout = QVBoxLayout()
        self.populate_categories_ui()
        layout.addLayout(self.categories_layout)

        # Save file name input
        filename_layout = QFormLayout()
        self.filename_input = QLineEdit(self.default_filename)
        filename_layout.addRow("Filename:", self.filename_input)
        layout.addLayout(filename_layout)

        # Generate button
        self.generate_button = QPushButton("Generate Template")
        self.generate_button.clicked.connect(self.generate_template)
        layout.addWidget(self.generate_button)

        # Add category button
        self.add_category_button = QPushButton("Add Category")
        self.add_category_button.clicked.connect(self.add_category_ui)
        layout.addWidget(self.add_category_button)

    def populate_categories_ui(self):
        """
        Populates the UI with existing categories and metrics.
        """
        for category, metrics in self.categories.items():
            self.add_category_ui(category, metrics)

    def add_category_ui(self, category_name=None, metrics=None):
        """
        Adds a category UI with associated metrics.
        """
        if category_name is None:
            category_name = f"Category {len(self.categories) + 1}"
            self.categories[category_name] = []
            metrics = []

        # Create UI elements
        category_label = QLabel(category_name)
        category_label.setAlignment(Qt.AlignLeft)

        metrics_combobox = QComboBox()
        metrics_combobox.addItems(metrics)

        metric_input = QLineEdit()
        add_metric_button = QPushButton("Add Metric")
        add_metric_button.clicked.connect(
            lambda: self.add_metric(metrics_combobox, metric_input, category_name)
        )

        category_layout = QGridLayout()
        category_layout.addWidget(category_label, 0, 0)
        category_layout.addWidget(metrics_combobox, 0, 1)
        category_layout.addWidget(metric_input, 1, 0)
        category_layout.addWidget(add_metric_button, 1, 1)

        self.categories_layout.addLayout(category_layout)

    def add_metric(self, combobox, input_field, category_name):
        """
        Adds a metric to the combobox and updates the categories dictionary.
        """
        new_metric = input_field.text().strip()
        if new_metric:
            combobox.addItem(new_metric)
            self.categories[category_name].append(new_metric)
            input_field.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Metric cannot be empty.")

    def generate_template(self):
        """
        Generates a feedback template based on user inputs.
        """
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Template",
            self.filename_input.text(),  # Use user-provided filename as default
            "Word Documents (*.docx)",
        )

        if filename:
            reviewer_name = self.reviewer_name_input.text().strip()
            group_name = self.group_name_input.text().strip()
            researcher_name = self.researcher_name_input.text().strip()

            # if not reviewer_name or not group_name or not researcher_name:
            #     QMessageBox.warning(
            #         self,
            #         "Missing Information",
            #         "Please fill out Reviewer Name, Group Name, and Researcher Name.",
            #     )
            #     return

            generator = TemplateGenerator()#self.categories)
            generator.generate_template(
                filename,
                reviewer_name=reviewer_name,
                group_name=group_name,
                researcher_name=researcher_name,
            )
            QMessageBox.information(self, "Success", f"Template saved as {filename}")
        else:
            QMessageBox.warning(self, "Save Canceled", "No file was saved.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = TemplateDialog()
    dialog.exec_()
