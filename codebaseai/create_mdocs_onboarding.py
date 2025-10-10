import logging
import langchain_core.prompts as prompts
from codebaseai import run_chain

def create_mdocs_onboarding(documentation, output_docs, model_name=None):
    """
    Creates an onboarding guide for new developers based on the documentation.
    Args:
        documentation (str): The documentation content to use for the onboarding guide.
    Returns:
        str: The AI-generated onboarding guide.
    Side Effects:
        Writes the onboarding guide to a file in the output directory.
        Logs the process of creating the onboarding guide.
    """
    logger = logging.getLogger(__name__)
    prompt = prompts.ChatPromptTemplate.from_template("""
        Here is the output of a mdocs analysis of the docstrings in this module.
        Create an onboarding guide for new developers based on the documentation.md. 
        Explain the codebase structure, key modules to focus on, and the typical development workflow.
        Documentation:
         {input}
        """
    )
    output_file_path = output_docs / "documentation_onboarding_ai.md"
    ai_response = ""
    with open(output_file_path, "w") as output_file:
        ai_response = run_chain(prompt, documentation, model_name)
        output_file.write(ai_response)
    logger.info(f"Documentation onboarding saved to {output_file_path}")
    return ai_response
