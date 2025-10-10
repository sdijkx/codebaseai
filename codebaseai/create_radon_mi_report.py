import os
import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain

def create_radon_mi_report(report, output_dir, model_name=None):
    """
    Creates a summary report for Radon MI analysis using AI.
    Args:
        report (str): The Radon MI analysis report content.
    Returns:
        str: The AI-generated summary of the Radon MI report.
    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a radon mi analysis report that measures the maintainability index of each file in a Python project.
        Please:
         - List the files with the lowest maintainability index scores.
         - Identify common patterns or reasons for low scores.
         - Suggest specific improvements for increasing maintainability (e.g., reducing complexity, adding comments, splitting large files).
         - Provide an overall assessment of the codebase’s maintainability.
        Report:
         {input}
        """
    )
    output_file_path = os.path.join(output_dir, "radon_mi_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report, model_name)
        output_file.write(ai_response)
    logger.info(f"Radon mi analysis summary saved to {output_file_path}")
    return ai_response
