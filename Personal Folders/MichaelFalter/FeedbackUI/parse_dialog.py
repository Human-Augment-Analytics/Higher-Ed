import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from docx import Document
import traceback


class ParseDialog(QDialog):
    """
    Dialog for selecting and parsing feedback templates.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parse Feedback Templates")
        self.setMinimumSize(600, 400)

        # Layout and widgets
        layout = QVBoxLayout(self)

        # Label
        self.label = QLabel("Select Word Documents (.docx) to parse feedback.")
        layout.addWidget(self.label)

        # Buttons
        self.select_button = QPushButton("Select Files")
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)

        # Table for displaying parsed data
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Adjust based on parsed data
        self.table.setHorizontalHeaderLabels(["Category", "Metric", "Score"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Parse button
        self.parse_button = QPushButton("Parse Selected Files")
        self.parse_button.clicked.connect(self.parse_files)
        self.parse_button.setEnabled(False)  # Disabled until files are selected
        layout.addWidget(self.parse_button)

        # Storage for selected files
        self.selected_files = []

    def select_files(self):
        """
        Open a file dialog to select .docx files.
        """
        files, _ = QFileDialog.getOpenFileNames(self, "Select Word Documents", "", "Word Documents (*.docx)")
        if files:
            self.selected_files = files
            self.label.setText(f"{len(files)} file(s) selected.")
            self.parse_button.setEnabled(True)

    def parse_files(self):
        """
        Parse the selected Word documents and display extracted data in the table.
        """
        try:
            parsed_data = []
            for file in self.selected_files:
                data = self.parse_feedback_doc(file)
                parsed_data.extend(data)

            # Populate the table with parsed data
            self.populate_table(parsed_data)
            QMessageBox.information(self, "Parsing Complete", f"Parsed {len(self.selected_files)} file(s) successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Parsing Error", f"An error occurred: {str(e)}")
            traceback.print_exc()

    def parse_feedback_doc(self, doc_path):
        """
        Parses a single Word document and extracts relevant data.

        Parameters:
            doc_path (str): Path to the .docx file.

        Returns:
            list: A list of dictionaries containing parsed feedback data.
        """
        doc = Document(doc_path)
        parsed_data = []

        for table in doc.tables:
            for row in table.rows[1:]:  # Skip the header row
                cells = row.cells
                if len(cells) >= 3:  # Ensure enough columns exist
                    category = cells[0].text.strip()
                    metric = cells[1].text.strip()
                    score = cells[2].text.strip()

                    parsed_data.append({
                        "Category": category,
                        "Metric": metric,
                        "Score": score
                    })

        return parsed_data

    def populate_table(self, data):
        """
        Populate the table with parsed data.

        Parameters:
            data (list): A list of dictionaries containing parsed data.
        """
        self.table.setRowCount(len(data))
        for row_idx, entry in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(entry["Category"]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(entry["Metric"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(entry["Score"]))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ParseDialog()
    dialog.exec_()
