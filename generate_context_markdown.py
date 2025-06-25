import os
from pathlib import Path
from datetime import datetime

def generate_context_markdown(output_filename: str = "project_context.md"):
    """
    Combines project information and code files into a single Markdown file
    for AI context preservation.
    """
    # Assumes this script is in a 'scripts/' subdirectory within the project root.
    # Adjust `Path(__file__).parent.parent` if your structure is different.
    project_root = Path(__file__).parent.parent 
    
    # --- SECTION 1: Project Overview (from README.md) ---
    readme_path = project_root / "README.md"
    readme_content = ""
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")
    else:
        readme_content = "## Project Overview\n\nREADME.md not found. Please create one with project description."

    # --- SECTION 2: Chronological List of Issues/Requirements ---
    # IMPORTANT: This section needs to be manually populated by you
    # based on our conversation history. It's a placeholder.
    issues_content_placeholder = """
## Chronological List of Issues/Requirements & Resolutions

This section summarizes the issues encountered and the solutions implemented throughout the project's development. This is crucial for understanding the rationale behind the current codebase.

---

**[ISSUE 1 TITLE/SUMMARY]**
* **Description:** [Original description of the issue from our conversation, e.g., "The difficulty label should only be one of 'Easy', 'Medium', 'Hard', and 'Impossible'."]
* **Status:** [Addressed/Pending]
* **Resolution/Discussion:** [How it was addressed, e.g., "Implemented `VALID_DIFFICULTY_LABELS` and validation in `InfoFileManager`."]
* **Reference (if applicable):** [e.g., "Covered in turn X of the conversation."]

---

**[ISSUE 2 TITLE/SUMMARY]**
* **Description:** [Original description of the issue]
* **Status:** [Addressed/Pending]
* **Resolution/Discussion:** [How it was addressed]
* **Reference (if applicable):**

---

*(Continue adding more issues in chronological order as they were discussed/resolved)*

---

## Key Design Decisions

* **Beat Count Handling:** The `beat_count` is passed as a parameter to `InfoFileManager.add_difficulty_entry` rather than being automatically calculated by `InfoFileManager`. This maintains a clear separation of concerns, keeping `InfoFileManager` focused on metadata and preventing it from needing to parse beatmap content.
* **Private Path Configuration:** Local game installation paths are stored in `game_paths.py` (or `local_config.py`) and are Git-ignored. This improves portability and security.

"""

    # --- SECTION 3: Current Codebase ---
    # List of files to include in the context, relative to the project root
    code_files = [
        "beatmap_editor.py",
        "beatmap_event_manager.py",
        "info_file_manager.py",
        "scripts/generate_zombie_beatmap.py",
        "main_beatmap_app.py",
        "game_paths.py", # This file should exist for the AI to see the structure
        ".gitignore"
    ]

    codebase_content = "## Current Codebase Files\n\n"
    for file_path_str in code_files:
        file_path = project_root / file_path_str
        if file_path.exists():
            # Determine language for markdown code block
            lang = "python"
            if file_path_str.endswith(".gitignore"):
                lang = "text" # .gitignore is plain text
            
            codebase_content += f"### File: `{file_path_str}`\n\n"
            codebase_content += f"```{lang}\n"
            codebase_content += file_path.read_text(encoding="utf-8")
            codebase_content += f"\n```\n\n"
        else:
            codebase_content += f"### File: `{file_path_str}` - NOT FOUND (Please ensure it exists in your project root or `scripts/`)\n\n"

    # --- Combine all sections ---
    full_context_content = f"""
# Project Context for AI Assistant

**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document consolidates all necessary information for an AI assistant to understand the "Crypt of the NecroDancer Custom Beatmap Generator" project. It includes the project overview, a chronological list of issues and their resolutions, key design decisions, and the full current codebase.

{readme_content}

{issues_content_placeholder}

{codebase_content}

## Instructions for AI Assistant

* Always refer to the provided codebase files as the authoritative source for the project's current state.
* When proposing changes, indicate which file(s) are affected and provide clear diffs or updated code blocks.
* Prioritize addressing issues chronologically as listed, or as directed by the user in the current conversation.
* Maintain the established code style and structure.
* Be mindful of the design decisions outlined above.
"""

    with open(project_root / output_filename, "w", encoding="utf-8") as f:
        f.write(full_context_content.strip())

    print(f"\nSuccessfully generated '{output_filename}' in the project root directory.")
    print("Please review the content, especially the 'Chronological List of Issues/Requirements' section,")
    print("and fill in the details manually based on our conversation history.")
    print("\nWhen starting a new conversation with an AI, copy the *entire content* of this file into the prompt.")


if __name__ == "__main__":
    # Ensure this script is run from within the 'scripts' directory
    # or adjust `project_root` accordingly if it's run from the main project root.
    # For example, if you run `python scripts/generate_context_markdown.py`
    # and your project structure is:
    # my_project/
    # ├── scripts/
    # │   └── generate_context_markdown.py
    # └── README.md
    # └── beatmap_editor.py
    # etc.
    # The `Path(__file__).parent.parent` correctly navigates up to `my_project/`.
    
    generate_context_markdown()