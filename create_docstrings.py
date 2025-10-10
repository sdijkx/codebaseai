"""
This script analyzes a codebase and generates reports by adding docstrings to Python scripts using AI. 
It utilizes OpenAI's language model to improve the readability and maintainability of the codebase by 
automatically generating docstrings for functions and classes in the scripts.

The script requires an OpenAI API key to function, which should be set in the environment variables.
"""

import os
import sys
import argparse
import re

import logging
from langchain_core.prompts import ChatPromptTemplate
import json
from pathlib import Path
import dotenv
from codebaseai import setup_logger, get_path as get_directory_path_or_exit
import codebaseai

exclude = ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.env']

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create reports based on the analysis of a codebase using AI.")
    parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase (module level) to analyze.")
    parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
    parser.add_argument("-t", "--title", default="Repository documentation", help="Title of the documentation")
    parser.add_argument("-d", "--developer", default="Personal", help="Name of the developer / owner")
    parser.add_argument("-e", "--email", default="", help="E-mail address")
    parser.add_argument("-u", "--url", default="", help="URL of the website / repository")
    parser.add_argument("-D", "--description", default="AI-generated documentation", help="Short description on the documentation")
    parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
    parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
    parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
    parser.add_argument("-m", "--model_name", default="", help="default model name.")
    parser.add_argument("-M", "--llm_name", default='', help="default lmm.")
    parser.add_argument("-P", "--python", default="T", help="Create also docstrings, not only create markdown files (T/F)")
    return parser.parse_args()




def main():
    """
    Main function to add docstrings to Python scripts in a codebase using OpenAI.

    Side Effects:
        Logs the analysis process.
        Exits the program if the codebase directory does not exist.

    Raises:
        SystemExit: If the codebase directory does not exist.
    """
    try:
        dotenv.load_dotenv()
        args = parse_args()

        #initialize logger
        setup_logger(args.log_file, args.log_level,args.log_silent)

        # Load the specified LLM module
        codebaseai.import_llm_module(args.llm_name, args.model_name)

        codebase_dir = get_directory_path_or_exit(args.codebase_dir)
        output_dir = get_directory_path_or_exit(args.output_dir, create_if_not_exists=True)
        output_code = Path(os.path.join(output_dir, os.path.basename(os.path.abspath(codebase_dir))))
        output_docs = Path(os.path.join(output_code, "docs"))

        # Ensure output directory exists
        os.makedirs(output_docs, exist_ok=True)

        title = args.title
        developer = args.developer
        mail = args.email
        link = args.url
        description = args.description

        if not os.path.exists(codebase_dir):
            logger.error(f"Error: Directory {codebase_dir} does not exist.")
            sys.exit(1)

        if args.python in ['T', 't']:
            logger.info(f"Analyzing scripts at: {codebase_dir}")
            logger.info(f"Scripts with docstrings will be saved to: {output_dir}")
            for root, dirs, files in os.walk(codebase_dir, topdown=True):
                dirs[:] = [d for d in dirs if d not in exclude]
                for file in files:
                    if file.endswith(".py"):
                        script_path = Path(os.path.join(root, file))
                        output_path = output_code / os.path.relpath(script_path, codebase_dir)
                        codebaseai.create_docstrings(script_path, output_path)

        logger.info("Creating mdocs file")
        config = {"title": f"{title}", "description": f"{description}", "developer": f"{developer}", "mail": f"{mail}", "link": f"{link}"}
        codebaseai.process_mdocs(config, codebase_dir, output_docs)
        documentation_path = output_docs / "documentation.md"
        if os.path.exists(documentation_path):
            with open(documentation_path, "r") as doc_file:
                documentation = doc_file.read()
            logger.info("Creating report")
            codebaseai.create_mdocs_report(documentation, output_docs=output_docs)
            logger.info("Creating onboarding")
            codebaseai.create_mdocs_onboarding(documentation, output_docs=output_docs)
        else:
            logger.error(f"Error: {documentation_path} does not exist.")
    
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()