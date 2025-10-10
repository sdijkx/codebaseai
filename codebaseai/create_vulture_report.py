import os
import logging
import langchain_core.prompts as prompts
import codebaseai.llm_module as llm_module

def create_vulture_report(report, output_dir, model_name=None):
    """
    Creates a summary report for Vulture analysis using AI.
    Args:
        report (str): The Vulture analysis report content.
    Returns:
        str: The AI-generated summary of the Vulture report.
    Side Effects:
        Writes the summary to a markdown file in the output directory.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a vulture analysis report that lists unused code, functions, and variables in a Python project.
        Please:
         - Summarize the unused functions, variables, and classes.
         - Identify any critical-looking unused code that might need further investigation.
         - Suggest which unused code can likely be removed safely and which might need a review for hidden dependencies
        Report:
         {input}
        """
    )
    output_file_path = os.path.join(output_dir, "vulture_analysis_summary_ai.md")
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = llm_module.run_chain(prompt, report, model_name=model_name)
        output_file.write(ai_response)
    logger.info(f"Vulture analysis summary saved to {output_file_path}")
    return ai_response
