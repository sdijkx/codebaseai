"""
This script analyzes a codebase using various tools to assess code quality, complexity, and maintainability.
It utilizes tools such as Vulture, Pylint, and Radon to generate reports on unused code, code quality, and
code complexity. The results are saved in specified output directories for further review.
"""

import os
import sys
import argparse
import logging
from codebaseai import run_command, setup_logger

# Create a logger object
logger = logging.getLogger(__name__)


# Parse command line arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a codebase using various tools.")
    parser.add_argument("-c", "--codebase_dir", required=True, help="The directory of the codebase to analyze.")
    parser.add_argument("-o", "--output_dir", required=True, help="The directory to save the analysis reports.")
    parser.add_argument("-l", "--log_file", default='./analysis.log', help="The file to save the log.")
    args = parser.parse_args()
    return args


def analyze_with_vulture(output_dir: str, codebase_dir: str):
    """
    Finds unused code using Vulture.

    Side Effects:
        Generates a report on unused code and saves it to the output directory.
        Logs the process of running Vulture.
    """
    logger.info("Running vulture...")
    output_file = os.path.join(output_dir, "vulture_report.txt")
    command = f"vulture {codebase_dir}"
    run_command(command, output_file, logger)

def analyze_with_pylint(output_dir: str, codebase_dir: str):
    """
    Checks code quality with Pylint.

    Side Effects:
        Generates a code quality report and saves it to the output directory.
        Logs the process of running Pylint.
    """
    logger.info("Running pylint...")
    output_file = os.path.join(output_dir, "pylint_report.txt")
    command = f"pylint {codebase_dir} --output-format=text"
    run_command(command, output_file, logger)

def analyze_with_radon(output_dir: str, codebase_dir: str):
    """
    Analyzes code complexity and maintainability using Radon.

    Side Effects:
        Generates reports on cyclomatic complexity and maintainability index.
        Saves the reports to the output directory.
        Logs the process of running Radon.
    """
    logger.info("Running radon cc (Cyclomatic Complexity)...")
    cc_output = os.path.join(output_dir, "radon_cc_report.txt")
    command_cc = f"radon cc {codebase_dir} -a -s"
    run_command(command_cc, cc_output, logger)

    logger.info("Running radon mi (Maintainability Index)...")
    mi_output = os.path.join(output_dir, "radon_mi_report.txt")
    command_mi = f"radon mi {codebase_dir} -s"
    run_command(command_mi, mi_output, logger)

def main():
    """
    Main function to run all analysis tools.

    Side Effects:
        Checks the existence of the codebase directory.
        Runs Vulture, Pylint, and Radon analyses.
        Logs the overall process and results of the analysis.
        Exits the program if the codebase directory does not exist.
    """
    args = parse_args()
    # Configure logging
    setup_logger(args.log_file, logging.DEBUG, True)

    # Define the codebase directory to analyze and the output directory
    codebase_dir = args.codebase_dir
    output_dir = args.output_dir
    if not output_dir.endswith('/'):
        output_dir += '/'

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(codebase_dir):
        logger.error(f"Error: Directory {codebase_dir} does not exist.")
        sys.exit(1)

    logger.info(f"Analyzing codebase at: {codebase_dir}")
    logger.info(f"Reports will be saved to: {output_dir}")

    # Run analysis tools
    analyze_with_vulture(output_dir, codebase_dir)
    analyze_with_pylint(output_dir, codebase_dir)
    analyze_with_radon(output_dir, codebase_dir)

    logger.info(f"Code analysis completed. Check the reports in the '{output_dir}' folder.")

if __name__ == "__main__":
    main()