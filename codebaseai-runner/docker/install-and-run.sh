#!/bin/bash
cd codebaseai

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

echo "Installed package versions:"
vulture --version
pylint --version
radon --version

echo "Running analysis on example_project..."

echo "1. Run the script:"
python analyse_codebase.py -c /app/project -o /app/reports -l /app/reports/log.txt

echo "2. View the generated reports in the analysis_reports directory:"
echo "   - vulture_report.txt: Lists unused code."
echo "   - pylint_report.txt: Provides linting issues and code quality feedback."
echo "   - radon_cc_report.txt: Shows cyclomatic complexity."
echo "   - radon_mi_report.txt: Shows maintainability index."
echo ""
echo "Running ChatGPT on reports..."
echo "1. Run the script:"

echo "Create reports"
python create_reports.py -r /app/reports -o /app/reports -l /app/reports/log.txt

echo "Create README"
python create_readme.py -c /app/project -o /app/project_readme

echo "Create docstrings"
python create_docstrings.py -c /app/project -o /app/project_docstring

echo "Refactor java code"
python refactor_java.py -j /app/java_project -o /app/java_project_refactored