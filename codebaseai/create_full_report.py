import os
import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain

def create_full_report(report, output_dir, model_name=None):
    """
    Creates a full summary report combining all analysis reports using AI.
    Args:
        report (str): The combined content of all analysis reports.
    Returns:
        str: The AI-generated full summary report.
    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a full analysis report that includes vulture, pylint, radon cc, and radon mi reports for a Python project.
        Please:
         - Summarize the key findings from each report.
         - Identify common issues across the reports and suggest high-level strategies for improvement.
         - Provide an overall assessment of the codebase’s quality, complexity, and maintainability.
        Report:
         {input}
        """
    )
    output_file_path = os.path.join(output_dir, "full_analysis_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, report, model_name)
        output_file.write(ai_response)
    logger.info(f"Full analysis summary saved to {output_file_path}")
    return ai_response
