import os
import sys
import argparse
import logging
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from codebaseai import create_readme, import_llm_module, setup_logger, get_path as get_directory_path_or_exit
from dotenv import load_dotenv

"""
This script analyzes a codebase and creates or updates a README.md file using AI. 
It extracts information from various files in the codebase and uses an AI model to generate a comprehensive README.md.
"""

EXCLUDE = ['.git', '__pycache__', 'venv', 'node_modules', '.idea', '.vscode', '.pytest_cache', '.mypy_cache', '.env']
logger = logging.getLogger(__name__)

# Parse command line arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create / update README based on the analysis of a codebase using AI.")
    parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase (module level) to analyze.")
    parser.add_argument("-o", "--output", required=True, help="The location of the README file.")
    parser.add_argument("-t", "--title", default="Repository documentation", help="Title of the documentation")
    parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
    parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
    parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
    parser.add_argument("-m", "--model_name", default="", help="default model name.")
    parser.add_argument("-M", "--llm_name", default="", help="default lmm.")
    args = parser.parse_args()
    return args

def analyse_codebase(codebase_dir: Path, title: str):

    """
    Analyzes the codebase and prepares input text for README generation.
    Args:
        codebase_dir (Path): The directory of the codebase to analyze.
        title (str): The title of the documentation.
    Returns:
        str: The prepared input text for README generation.
    Side Effects:
        Logs the analysis process.
    """

    logger.info(f"Analyzing codebase at: {codebase_dir}")

    input_text = f"$$$$$ Title:  {title} $$$$$\n\n"
    readme_text = "$$$$$ NO EXISTING README.md, please create new one $$$$$\n"

    for root, dirs, files in os.walk(codebase_dir,topdown=True):

        dirs[:] = [d for d in dirs if d not in EXCLUDE]

        for file in files:
            file_path = Path(root) / Path(file)
            print(f"Processing file: {file_path}")
            if file == "README.md":
                with open(file_path, "r") as readme_file:
                    readme_text = f"\n$$$$$ Existing README.md $$$$$\n" + readme_file.read() + f"\n$$$$$ End of existing README.md $$$$$\n"
            if file == "LICENSE":
                with open(file_path, "r") as license_file:
                    input_text += f"\n$$$$$ License file {file} $$$$$\n" + license_file.read() + f"\n$$$$$ End of license file {file} $$$$$\n"

            if file_path.name.endswith(".md") and file_path.name != "README.md":
                with open(file_path, "r") as doc_file:
                    input_text += f"\n$$$$$ Documentation file {file} $$$$$\n" + doc_file.read() + f"\n$$$$$ End of documentation file {file} $$$$$\n"

            if file_path.name.endswith(".py"):
                with open(file_path, "r") as python_file:
                    python_script = python_file.read()
                    if "__main__" in python_script:
                        input_text += f"\n$$$$$ Python script {file} $$$$$\n" + python_script + f"\n$$$$$ End of Python script {file} $$$$$\n"
            if file_path.name == "requirements.txt":
                with open(file_path, "r") as req_file:
                    input_text += f"\n$$$$$ Requirements file {file} $$$$$\n" + req_file.read() + f"\n$$$$$ End of requirements file {file} $$$$$\n"

            input_text += readme_text

    return input_text


def main():
    """
    Main function to analyze the codebase and generate or update the README.md file.

    Side Effects:
        - Logs the analysis process and any errors encountered.
        - Calls the create_readme function to generate the README.md content.
    """
    try:
        load_dotenv()
        args = parse_args()
        #initialize logger
        setup_logger(args.log_file, args.log_level,args.log_silent)

        #import ai module
        import_llm_module(args.llm_name, args.model_name)


        codebase_dir = get_directory_path_or_exit(args.codebase_dir)
        output_doc = Path(args.output)

        if not "README.md" in str(output_doc):
            output_doc /= 'README.md'

        if not output_doc.parent.exists():
            os.makedirs(output_doc.parent)

        if not os.path.exists(codebase_dir):
            logger.error(f"Error: Directory {codebase_dir} does not exist.")
            sys.exit(1)

        title = args.title

        input_text = analyse_codebase(codebase_dir, title)

        logger.info(f"creating README.md: {output_doc}")
        create_readme(input_text, output_doc)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()