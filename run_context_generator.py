from generate_context_markdown import generate_context_markdown

# --- Project-Specific Configuration ---
# Change these values for each project you use this script in.

# The name of your project.
PROJECT_NAME = "New Project"

# A list of specific markdown files to include in the preamble.
OPTIONAL_DOCS_TO_INCLUDE = [
    "docs/project_issues.md",
]

# A list of folders to scan recursively for .md files to include.
DOC_FOLDERS_TO_SCAN = [
    "docs/api_reference",
]

# A list of specific files to explicitly exclude from the context.
FILES_TO_EXCLUDE = [
    "package-lock.json",
]

# A list of folders to explicitly exclude from the context.
# Add any folder here to prevent it from being scanned.
FOLDERS_TO_EXCLUDE = [
    # VCS
    ".git",
    # IDEs / Editors
    ".vscode",
    ".idea",
    # Language-specific
    "node_modules",
    ".venv",
    "__pycache__",
    # Build artifacts
    "dist",
    "build",
    # To include .husky, simply comment out or remove the next line.
    ".husky", 
]

# The maximum number of characters for each output file.
MAX_CHARACTERS = 500000

# Whether to split the output into multiple files if it exceeds the character limit.
SPLIT_FILES = True

# --------------------------------------

if __name__ == "__main__":
    """
    Runs the AI context generator with the configuration defined above.
    """
    print("--- Starting AI Context Generation ---")
    
    generate_context_markdown(
        project_name=PROJECT_NAME,
        optional_docs=OPTIONAL_DOCS_TO_INCLUDE,
        doc_folders=DOC_FOLDERS_TO_SCAN,
        exclude_files=FILES_TO_EXCLUDE,
        exclude_folders=FOLDERS_TO_EXCLUDE,
        max_output_characters=MAX_CHARACTERS,
        split_output_if_truncated=SPLIT_FILES
    )
    
    print("\n--- AI Context Generation Complete ---")