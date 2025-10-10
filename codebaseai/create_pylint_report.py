import os
import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain


def create_pylint_report(report, output_dir, model_name=None):
    """
    Creates a summary report for Pylint analysis using AI.
    Args:
        report (str): The Pylint analysis report content.
    Returns:
        str: The AI-generated summary of the Pylint report.
    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a pylint analysis report that highlights code quality issues in a Python project.
        Please:
         - Summarize the most frequent and severe linting issues (e.g., errors, warnings, and convention violations).
         - Group the issues by type and explain their impact on code quality.
         - Suggest specific fixes or refactoring strategies for the most critical issues.
         - Provide an overall quality assessment of the codebase based on this report.
        Report:
         {input}
        """
    )
    output_file_path = os.path.join(output_dir, "pylint_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report, model_name)
        output_file.write(ai_response)
    logger.info(f"Pylint analysis summary saved to {output_file_path}")
    return ai_response
