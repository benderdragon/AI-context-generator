import os
from pathlib import Path
from datetime import datetime
import re
from typing import List, Tuple

def generate_context_markdown(
    output_filename: str = "project_context.md",
    project_name: str = "Unnamed Project", # New parameter for project name
    readme_filename: str = "README.md", # Parameterize README path
    issues_filename: str = "project_issues.md", # Parameterize issues path
    design_decisions_filename: str = "project_design_decisions.md", # Parameterize design decisions path
    ai_instructions_filename: str = "ai_instructions.md" # Parameterize AI instructions path
):
    """
    Combines project information and code files into a single Markdown file
    for AI context preservation.
    
    Args:
        output_filename (str): The name of the output Markdown file.
        project_name (str): The name of the project.
        readme_filename (str): The filename of the project's README.
        issues_filename (str): The filename containing chronological issues/requirements.
        design_decisions_filename (str): The filename containing key design decisions.
        ai_instructions_filename (str): The filename containing AI assistant instructions.
    """
    project_root = Path(__file__).parent.parent 
    
    # --- SECTION 1: Project Overview (from README.md) ---
    readme_path = project_root / readme_filename
    readme_content = ""
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")
    else:
        readme_content = f"## Project Overview\n\n`{readme_filename}` not found. Please create one with project description."

    # --- SECTION 2: Chronological List of Issues/Requirements (from project_issues.md) ---
    issues_path = project_root / issues_filename
    issues_content = ""
    if issues_path.exists():
        issues_content = issues_path.read_text(encoding="utf-8")
    else:
        issues_content = f"## Chronological List of Issues/Requirements & Resolutions\n\n`{issues_filename}` not found. Please create one with project issues and resolutions."

    # --- SECTION 3: Key Design Decisions (from project_design_decisions.md) ---
    design_decisions_path = project_root / design_decisions_filename
    design_decisions_content = ""
    if design_decisions_path.exists():
        design_decisions_content = design_decisions_path.read_text(encoding="utf-8")
    else:
        design_decisions_content = f"## Key Design Decisions\n\n`{design_decisions_filename}` not found. Please create one with key design decisions."

    # --- SECTION 4: Instructions for AI Assistant (from ai_instructions.md) ---
    ai_instructions_path = project_root / ai_instructions_filename
    ai_instructions_content = ""
    if ai_instructions_path.exists():
        ai_instructions_content = ai_instructions_path.read_text(encoding="utf-8")
    else:
        ai_instructions_content = f"## Instructions for AI Assistant\n\n`{ai_instructions_filename}` not found. Please create one with instructions for the AI assistant."

    # Function to parse .gitignore and return a list of regex patterns
    def get_gitignore_patterns(gitignore_path: Path) -> List[Tuple[re.Pattern, bool]]:
        patterns = []
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    is_negated = line.startswith('!')
                    if is_negated:
                        line = line[1:] # Remove '!'
                    
                    # Convert .gitignore patterns to regex
                    # Escape special characters that are not * or ?
                    pattern_str = re.escape(line)
                    # Convert * to .* (any characters)
                    pattern_str = pattern_str.replace(r'\*', '.*')
                    # Convert ? to . (any single character)
                    pattern_str = pattern_str.replace(r'\?', '.')
                    
                    # Handle directory patterns (ending with /)
                    if line.endswith('/'):
                        # Match directory itself and its contents
                        pattern_str += '.*' 
                    # If pattern is just a name (e.g., 'foo'), it matches files and dirs named 'foo' anywhere
                    elif '/' not in line:
                         pattern_str = f"(^|.*/){pattern_str}" 
                    
                    # Handle anchoring to project root (patterns starting with '/')
                    if line.startswith('/'):
                        pattern_str = pattern_str.lstrip(r'\/') # Remove escaped leading slash
                        pattern_str = f"^{pattern_str}" # Anchor to start of relative path
                    
                    patterns.append((re.compile(pattern_str), is_negated))
        return patterns

    # Get .gitignore patterns
    gitignore_path = project_root / ".gitignore"
    ignore_patterns = get_gitignore_patterns(gitignore_path)

    code_files: List[str] = []
    
    # Function to check if a file path should be ignored
    def should_ignore(relative_path: Path) -> bool:
        path_str = str(relative_path).replace("\\", "/") # Standardize path separators
        
        # Paths that are always ignored regardless of .gitignore
        # This prevents including the context file itself or the generation script
        if relative_path == Path(output_filename) or \
           relative_path == Path(__file__).relative_to(project_root) or \
           relative_path == Path(readme_path).relative_to(project_root) or \
           relative_path == Path(issues_path).relative_to(project_root) or \
           relative_path == Path(design_decisions_path).relative_to(project_root) or \
           relative_path == Path(ai_instructions_path).relative_to(project_root):
            return True

        # Track the last match: True if ignored, False if negated
        final_decision_is_ignored = False

        for pattern_regex, is_negated in ignore_patterns:
            # Check if the full relative path matches the pattern
            if pattern_regex.fullmatch(path_str):
                if is_negated:
                    final_decision_is_ignored = False # A negation overrides previous ignores
                else:
                    final_decision_is_ignored = True # An ignore pattern matches
            # If the pattern doesn't contain a slash, check if it matches the basename
            elif '/' not in pattern_regex.pattern.replace(r'.\*', ''): # Check original pattern part
                 if pattern_regex.fullmatch(os.path.basename(path_str)):
                    if is_negated:
                        final_decision_is_ignored = False
                    else:
                        final_decision_is_ignored = True


        return final_decision_is_ignored

    # Walk the project directory to find all files
    for dirpath, dirnames, filenames in os.walk(project_root):
        current_relative_dir = Path(dirpath).relative_to(project_root)

        # Filter out ignored directories *before* walking into them
        # Create a copy of dirnames to iterate over while modifying the original list
        dirs_to_process = dirnames[:] 
        dirnames.clear() # Clear original list to fill with allowed ones

        for dname in dirs_to_process:
            relative_dir_path = current_relative_dir / dname
            # Do not traverse into hidden directories (like .git, .vscode, etc.) or any directory listed in .gitignore
            if dname.startswith('.') or should_ignore(relative_dir_path):
                continue
            dirnames.append(dname) # Only keep directories that are not ignored

        for filename in filenames:
            file_absolute_path = Path(dirpath) / filename
            file_relative_path = file_absolute_path.relative_to(project_root)
            
            # Check against .gitignore patterns and always-ignored files
            if not should_ignore(file_relative_path):
                code_files.append(str(file_relative_path).replace("\\", "/")) # Store with forward slashes

    codebase_content = "## Current Codebase Files\n\n"
    # Sort files for consistent output
    code_files.sort() 

    # --- New print statement for listed files ---
    print("\n--- Files included in project_context.md ---")
    for file_path_str in code_files:
        print(f"- {file_path_str}")
    print("-------------------------------------------\n")

    for file_path_str in code_files:
        file_path = project_root / file_path_str
        if file_path.exists():
            # Determine language for markdown code block
            lang = "text" # Default to text
            if file_path_str.endswith(".py"):
                lang = "python"
            elif file_path_str.endswith(".json"):
                lang = "json"
            elif file_path_str.endswith(".md"):
                lang = "markdown"
            elif file_path_str == ".gitignore":
                lang = "text" # Explicitly text for .gitignore
            
            codebase_content += f"### File: `{file_path_str}`\n\n"
            codebase_content += f"```{lang}\n"
            codebase_content += file_path.read_text(encoding="utf-8")
            codebase_content += f"\n```\n\n"
        else:
            # This 'else' block should ideally not be reached if should_ignore and os.walk are perfect
            codebase_content += f"### File: `{file_path_str}` - NOT FOUND (This should not happen if file exists on disk)\n\n"

    # --- Combine all sections ---
    full_context_content = f"""
# Project Context for AI Assistant - {project_name}

**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This document consolidates all necessary information for an AI assistant to understand the "{project_name}" project. It includes the project overview, a chronological list of issues and their resolutions, key design decisions, and the full current codebase.

{readme_content}

{issues_content}

{design_decisions_content}

{ai_instructions_content}

{codebase_content}

"""

    with open(project_root / output_filename, "w", encoding="utf-8") as f:
        f.write(full_context_content.strip())

    print(f"\nSuccessfully generated '{output_filename}' in the project root directory.")
    print("Please review the content.")
    print("\nWhen starting a new conversation with an AI, copy the *entire content* of this file into the prompt.")


if __name__ == "__main__":
    # Example usage for the "Rift of the NecroDancer Custom Beatmap Generator" project
    generate_context_markdown(
        project_name="Rift of the NecroDancer Custom Beatmap Generator",
        readme_filename="README.md", # Assuming README.md is in the project root
        issues_filename="project_issues.md", # Assuming project_issues.md is in the project root
        design_decisions_filename="project_design_decisions.md", # Assuming project_design_decisions.md is in the project root
        ai_instructions_filename="ai_instructions.md" # Assuming ai_instructions.md is in the project root
    )

    # For a new project, you could call it like this:
    # generate_context_markdown(
    #     project_name="My New Python App",
    #     issues_filename="my_app_issues.md", # If you have a different issues file
    #     design_decisions_filename="my_app_design.md", # If you have a different design file
    #     # Or omit arguments to use defaults for non-existent files:
    #     # issues_filename="non_existent_issues.md" 
    # )
    
    # Or for a super generic context without specific issues/design decisions:
    # generate_context_markdown(project_name="Generic Python Utility")