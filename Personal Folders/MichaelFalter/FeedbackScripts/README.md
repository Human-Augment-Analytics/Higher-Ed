# Research Feedback Analysis Tool

This tool provides a way to generate and analyze structured feedback on research reports. It includes two main scripts:

1. **Feedback Template Generator**: This script creates a standardized Word document template for reviewers to evaluate research quality across multiple categories, including:
   - **Clarity and Presentation Metrics**
   - **Content Understanding and Communication Metrics**
   - **Technical and Analytical Depth Metrics**
   - **Progress and Responsiveness Metrics**
   - **Engagement and Interaction Metrics**

   Each category contains individual metrics for which reviewers can provide scores (1-5) and comments. The generated template helps ensure consistent feedback collection across reports.

    Note: These categories are subject to change and by no means final. 

2. **Feedback Analysis Script**: This script reads completed feedback documents, organizes the data by category, and calculates average feedback scores across weeks or semesters. Key features include:
   - **Weekly Averages**: Calculates and organizes average feedback scores for each metric by week. Currently either line charts by semester over weeks or bar charts for all categories by Semester+Week.

Note: These visualizations are still being worked on.

## Installation

To use this tool, install the following dependencies:

```bash
pip install python-docx pandas matplotlib
```

## Example Workflow

1. **Generate the Feedback Template**: Run the template generator script to create the `Research_Feedback_Template.docx` file.
2. **Collect Feedback**: Distribute the template to reviewers, have them complete it, and save the filled forms in a designated folder.
3. **Analyze Feedback**: Run the analysis script to process the feedback files (all of which should be in the same directory the script is run from), calculate weekly averages, and visualize the results.

## Notes

- Ensure all feedback files follow the provided template structure.
- The feedback template includes fields for reviewer and researcher details, along with scoring and comments for each feedback metric in each category. Not all of these fields are currently being used in the parser script.
- The analysis tool assumes that scores are provided on a 1-5 scale. Decide amongst your group how to best follow this scale.
- The current date structure is expected to be 'Semester, Week' such as 'Fall 24, Week 12'.
