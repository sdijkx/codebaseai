import os
import sys
import logging
import argparse
from dotenv import load_dotenv
from codebaseai import run_command, extract_and_refactor_methods, create_connection, import_llm_module, setup_logger, get_path, for_each_file

"""
This script refactors Java code using AI. It processes Java files in a specified directory, 
removes comments, extracts methods, refactors them using an AI model, and restores comments 
before saving the refactored code to an output directory. It also logs the process and handles 
command-line arguments for configuration.
"""

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Refactor Java code using AI.")
    parser.add_argument("-j", "--java_dir", required=True, help="The Java package(s) directory to refactor.")
    parser.add_argument("-o", "--output_dir", required=True, help="The directory to store the refactored source code.")
    parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
    parser.add_argument("-L", "--log_level", default='INFO', help="The loglevel.")
    parser.add_argument("-S", "--log_silent", help="Suppress the log to stdout.", action='store_false')
    parser.add_argument("-m", "--model_name", default="", help="default model name.")
    parser.add_argument("-M", "--llm_name", default="", help="default lmm.")
    parser.add_argument("-p", "--prompt", default="./refactoring_prompt.txt", help="The refactor prompt")
    args = parser.parse_args()
    return args


def main():
    """
    Main function to refactor Java code using AI.

    Side Effects:
        Refactors Java files in the specified directory and saves them to the output directory.
        Logs the refactoring process.
    """
    try:
        load_dotenv()
        args = parse_args()

        #initialize logger
        setup_logger(args.log_file, args.log_level,args.log_silent)

        #initialize ai 
        import_llm_module(args.llm_name, args.model_name)

        src_dir = get_path(args.java_dir)
        output_dir = get_path(args.output_dir, create_if_not_exists=True)
        
        connection = create_connection()
        with open(args.prompt, 'r', encoding='utf-8') as prompt_file:
            prompt_text = prompt_file.read()
        for file_path in for_each_file(src_dir, file_ext=".java"):
            output_file_path = output_dir / os.path.relpath(file_path, src_dir)
            if os.path.exists(output_file_path) and os.path.getmtime(file_path) < os.path.getmtime(output_file_path):
                logger.info(f"Skipping {file_path} as it is not newer than the existing output.")
            else:
                logger.info(f"Refactoring {file_path}.")
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                logger.debug(f"Refactoring {file_path} to {output_file_path} using prompt from {prompt_text}")
            
            #Refactor the code
                refactored_code = extract_and_refactor_methods(file_path, prompt_text, connection)
            
                with open(output_file_path, "w") as output_file:
                    output_file.write(refactored_code)
                    logger.info(f"Refactored code written to: {output_file_path}")
                run_command(f"astyle -n --style=java {output_file_path}", None, logger)
        logger.info("Refactoring completed.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
