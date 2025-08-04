from generate_context_markdown import generate_context_markdown

# --- Project-Specific Configuration ---
# Change these values for each project you use this script in.

# The name of your project.
PROJECT_NAME = "New Project"

# A list of specific markdown files to include in the preamble.
# These paths are relative to the project root.
OPTIONAL_DOCS_TO_INCLUDE = [
    "docs/project_issues.md",
]

# A list of folders to scan recursively for .md files to include.
DOC_FOLDERS_TO_SCAN = [
    "docs/api_reference", # Example folder for auto-generated docs
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
        max_output_characters=MAX_CHARACTERS,
        split_output_if_truncated=SPLIT_FILES
    )
    
    print("\n--- AI Context Generation Complete ---")