import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain

def create_mdocs_report(documentation, output_docs, model_name=None):
    """
    Generates a summary report of the documentation using AI.
    Args:
        documentation (str): The documentation content to summarize.
    Returns:
        str: The AI-generated summary of the documentation.
    Side Effects:
        Writes the summary to a file in the output directory.
        Logs the process of creating the summary.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Summarize the key functionalities and workflows described in this documentation.md. 
        Highlight the main modules, their responsibilities, and how they interact. 
        Additionally, point out any unique features or design patterns used.
        Documentation:
         {input}
        """
    )
    output_file_path = output_docs / "documentation_summary_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, model_name)
        output_file.write(ai_response)
    logger.info(f"Documentation summary saved to {output_file_path}")
    return ai_response
