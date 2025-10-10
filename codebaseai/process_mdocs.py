import logging
import json
from codebaseai.run_command import run_command

def process_mdocs(config, codebase_dir, output_docs):
    """
    Processes the mdocs settings and generates the documentation file.
    Side Effects:
        Writes the mdocs settings to a JSON file.
        Executes shell commands to generate and move the documentation file.
        Logs the process of generating the documentation.
    """
    logger = logging.getLogger(__name__)
    mdocs_settings_path = codebase_dir / "mdocs_settings.json"
    logger.info(f"Writing mdocs settings file to {mdocs_settings_path}")
    with open(mdocs_settings_path, "w") as settings_file:
        json.dump(config, settings_file, indent=4)
    documentation_path = codebase_dir / "documentation.md"
    documentation_target_path = output_docs / "documentation.md"
    logger.info(f"mdocs running on {codebase_dir.resolve()}")
    run_command(f"cd {codebase_dir.resolve()} && mdocs .", output_file=None, logger=logger)
    run_command(f"mv {documentation_path.resolve()} {documentation_target_path.resolve()}", output_file=None, logger=logger)
