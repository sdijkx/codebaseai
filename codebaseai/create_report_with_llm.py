import os
import logging
from codebaseai import create_vulture_report, create_pylint_report, create_radon_cc_report, create_radon_mi_report, create_full_report

def create_report_with_llm(report_dir, output_dir, model_name = None):
    """
    Generates analysis reports using OpenAI.
    Side Effects:
        Processes each report file in the report directory and generates corresponding AI summaries.
        Writes the summaries to markdown files in the output directory.
    """
    logger = logging.getLogger(__name__)
    full_report = ""
    # Generate reports for each file in the report directory
    for report_file in os.listdir(report_dir):
        logger.info(f"Processing report: {report_file}")
        if report_file.endswith(".txt"):
            report_path = os.path.join(report_dir, report_file)
            with open(report_path, "r") as f:
                report = f.read()
                if "vulture_report.txt" in report_file:
                    full_report += "Vulture Report:\n" + create_vulture_report(report, output_dir, model_name) + "\n\n"
                elif "pylint_report.txt" in report_file:
                    full_report += "Pylint Report:\n" + create_pylint_report(report, output_dir, model_name) + "\n\n"
                elif "radon_cc_report.txt" in report_file:
                    full_report += "Radon cc Report:\n" + create_radon_cc_report(report, output_dir, model_name) + "\n\n"
                elif "radon_mi_report.txt" in report_file:
                    full_report += "Radon mi Report:\n" + create_radon_mi_report(report, output_dir, model_name) + "\n\n"
    if len(full_report) > 0:
        create_full_report(full_report, output_dir, model_name)
    logger.info(f"Reports generated")
