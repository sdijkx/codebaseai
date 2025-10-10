import os
import sys
import importlib
import logging

logger = logging.getLogger(__name__)
llm_module = None

def import_llm_module(llm: str, llm_model: str) -> (str, str):
    """
    Loads the specified LLM module based on the provided name .

    Args:
        llm_name (str): The name of the LLM to load (e.g., 'open_ai', 'ollama').
        llm_model_name (str): The model name to use with the LLM.
    """
    try:
        global llm_module
        if not llm:
            llm = os.environ.get('LLM', 'open_ai')
            logger.info(f"Using default LLM: {llm}")
        else:
            logger.info(f"Using specified LLM model: {llm_model}")

        llm_module = importlib.import_module('codebaseai.ai_' + llm)
        if llm_model :
            llm_module.set_model(llm_model)

        logger.info(f"Using: module 'ai_{llm}' with model {llm_module.get_model()}.")
    
    except Exception as e:
        logger.error(f"Error loading module 'ai_{lmm}'.", e)
        sys.exit(1)


def run_chain(*args, **kwargs):
    """
    Runs the chain of runnables to process input data and generate an AI response.

    Passes all arguments to the loaded LLM module's run_chain function.

    Returns:
        the result of the LLM module's run_chain function.
    """
    if llm_module is None:
        logger.error("LLM module not loaded. Please load the LLM module first.")
        sys.exit(1)

    return llm_module.run_chain(*args, **kwargs)

def create_connection(*args, **kwargs):
    """
    Creates a connection to the specified LLM module.

    Passes all arguments to the loaded LLM module's create_connection function.

    Returns:
        the result of the LLM module's create_connection function.
    """
    return llm_module.create_connection(*args, **kwargs)
