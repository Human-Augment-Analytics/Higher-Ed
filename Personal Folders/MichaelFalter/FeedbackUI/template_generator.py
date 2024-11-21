from docx import Document
from docx.shared import Inches
import json

class TemplateGenerator:
    def __init__(self, categories=None):
        if categories is None:
            with open("categories.json", "r") as file:
                self.categories = json.load(file)
        else:
            self.categories = categories

    def generate_template(self, output_path, reviewer_name=None, group_name=None, researcher_name=None):
        doc = Document()
        doc.add_heading('Research Feedback Template', level=1)

        # Add reviewer and researcher info
        doc.add_paragraph(f"Reviewer Name: {reviewer_name or '________________'}")
        doc.add_paragraph(f"Researcher Name: {researcher_name or '________________'}")

        # Add categories and metrics
        for category, metrics in self.categories.items():
            doc.add_heading(category, level=2)
            table = doc.add_table(rows=1, cols=3)
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'Metric'
            hdr_cells[1].text = 'Score (1-5)'
            hdr_cells[2].text = 'Comments'

            for metric in metrics:
                row_cells = table.add_row().cells
                row_cells[0].text = metric

        doc.save(output_path)
        print(f"Template saved at {output_path}")
