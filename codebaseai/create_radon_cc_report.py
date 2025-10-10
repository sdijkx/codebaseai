import os
import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain

def create_radon_cc_report(report, output_dir, model_name=None):
    """
    Creates a summary report for Radon CC analysis using AI.
    Args:
        report (str): The Radon CC analysis report content.
    Returns:
        str: The AI-generated summary of the Radon CC report.
    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a radon cc analysis report that measures cyclomatic complexity for functions and methods in a Python project.
        Please:
         - Highlight the functions or methods with the highest complexity scores and explain their impact on maintainability.
         - Suggest ways to refactor or simplify the most complex functions/methods.
         - Provide a general summary of the codebase’s complexity and recommendations for improvement.
        Report:
         {input}
        """
    )
    output_file_path = os.path.join(output_dir, "radon_cc_report_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report, model_name)
        output_file.write(ai_response)
    logger.info(f"Radon cc analysis summary saved to {output_file_path}")
    return ai_response
