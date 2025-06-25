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
    issues_content = """
## Chronological List of Issues/Requirements & Resolutions

This section summarizes the issues encountered and the solutions implemented throughout the project's development. This is crucial for understanding the rationale behind the current codebase.

Only recent issues are mentioned. Some older issues may not appear.

---

**ISSUE 1: Difficulty Labels for `info.json` Entries**
* **Description:** The `info.json` file needs to accurately reflect the difficulty of a beatmap, and there should be a predefined set of valid difficulty labels (e.g., "Easy", "Medium", "Hard", "Impossible"). The system should validate against these labels to prevent arbitrary inputs.
* **Status:** Addressed
* **Resolution/Discussion:** A `VALID_DIFFICULTY_LABELS` class variable was added to `InfoFileManager`. The `add_difficulty_entry` method now explicitly checks the provided `difficulty_label` against this list and raises a `ValueError` if invalid. The `generate_zombie_beatmap` script was updated to ensure it passes a valid label.
* **Reference:** Discussed in various turns, specifically implemented in `info_file_manager.py` and utilized in `scripts/generate_zombie_beatmap.py`.

---

**ISSUE 2: `TrackLength` Management in `info.json`**
* **Description:** The `TrackLength` field in `info.json` (e.g., "0:00") should represent the actual duration of the audio track and not be dynamically changed or calculated by the beatmap generation process. It should be loaded from a template `info.json` and remain untouched.
* **Status:** Addressed
* **Resolution/Discussion:** The `_calculate_track_length` method was removed from `InfoFileManager`. The `TrackLength` field is now only loaded from the template `info.json` file and is explicitly excluded from modification logic in `add_difficulty_entry`. This ensures `InfoFileManager` focuses solely on metadata, not audio analysis.
* **Reference:** Implemented in `info_file_manager.py`.

---

**ISSUE 3: Correct `BeatCount` for `info.json` and Individual Difficulties**
* **Description:** The `BeatCount` in the `DifficultyInformation` entry should represent the total beats covered by that specific beatmap file (i.e., the `max_ending_beat_number + 1` from the beatmap events). Additionally, the top-level `BeatCount` in `info.json` should reflect the *longest* beatmap's beat count among all difficulties.
* **Status:** Addressed
* **Resolution/Discussion:** A `get_max_beat_number()` method was added to `BeatmapEventManager` to determine the highest beat used across all events. In `scripts/generate_zombie_beatmap.py`, this value is used to calculate the `beat_count` passed to `InfoFileManager.add_difficulty_entry`. The `add_difficulty_entry` method now updates the top-level `BeatCount` in `info_data` only if the new difficulty's `beat_count` is greater than the existing top-level `BeatCount`.
* **Reference:** Implemented in `beatmap_event_manager.py` and `info_file_manager.py`, utilized in `scripts/generate_zombie_beatmap.py`.

---

**ISSUE 4: Flexible BPM Handling for `DifficultyInformation`**
* **Description:** The BPM for a difficulty entry should ideally come from the specific beatmap being added. If not provided, it should default to the top-level `BeatsPerMinute` value in `info.json`. If that is also missing or zero, a sensible fallback (e.g., 120 BPM) should be used. Also, the top-level `BeatsPerMinute` should be set if it's currently 0 (indicating it's from a default empty template) when the first difficulty is added.
* **Status:** Addressed
* **Resolution/Discussion:** The `add_difficulty_entry` method in `InfoFileManager` now has an optional `bpm` parameter. If `bpm` is `None`, it retrieves the BPM from the top-level `_info_data.get("BeatsPerMinute")`. If that is also `None` or `<= 0`, it defaults to `120`. Furthermore, if the top-level `BeatsPerMinute` is `0`, it is updated with the `entry_bpm` of the first difficulty added.
* **Reference:** Implemented in `info_file_manager.py` and utilized in `scripts/generate_zombie_beatmap.py`.

---

**ISSUE 5: `track` Parameter Requirement for Spawn Events**
* **Description:** When adding `SpawnEnemy` or `SpawnTrap` events, the `track` parameter should be mandatory as enemies and traps are always placed on a specific track in-game. Previously, it might have been optional or had a default that didn't enforce this.
* **Status:** Addressed
* **Resolution/Discussion:** The `track` parameter in `add_spawn_enemy_event` and `add_spawn_trap_event` methods within `BeatmapEventManager` was made a mandatory argument without a default value, clearly indicating its necessity.
* **Reference:** Implemented in `beatmap_event_manager.py` and demonstrated in `main_beatmap_app.py` and `scripts/generate_zombie_beatmap.py`.

---

**ISSUE 6: Handling `start_beat_number` and `end_beat_number` for Events**
* **Description:** Event creation methods should be flexible, allowing users to provide either a `start_beat_number`, an `end_beat_number`, both, or neither. Default values should be sensible (e.g., `end_beat_number = start_beat_number + 1` if only `start_beat_number` is provided, and `start_beat_number = end_beat_number - 1` if only `end_beat_number` is provided, and `0, 1` if neither is provided).
* **Status:** Addressed
* **Resolution/Discussion:** The `add_spawn_enemy_event` and `add_spawn_trap_event` methods in `BeatmapEventManager` were updated to handle various combinations of `start_beat_number` and `end_beat_number` being `Optional[int]`. They now correctly calculate default values if one or both are omitted, ensuring valid beat ranges.
* **Reference:** Implemented in `beatmap_event_manager.py` and demonstrated in `main_beatmap_app.py`.

---

**ISSUE 7: Separation of `game_entity_definitions.json` and `game_trap_definitions.json`**
* **Description:** The game's entity definitions, particularly for enemies and traps, should be split into separate JSON files for clarity and easier management. This means `BeatmapEventManager` needs to load and access two distinct dictionaries for enemy IDs and trap IDs.
* **Status:** Addressed
* **Resolution/Discussion:** The `parse_lua_to_json.py` script was modified to output two separate JSON files: `game_entity_definitions.json` (for enemies and items) and `game_trap_definitions.json` (for traps). `BeatmapEventManager` was updated to load both these files into `ENEMY_NAMES` and `TRAP_NAMES` class variables, respectively, and provides `get_enemy_name` and `get_trap_name` methods for easy lookup.
* **Reference:** Implemented in `scripts/parse_lua_to_json.py` and `beatmap_event_manager.py`.

---

**ISSUE 8: Adding `SpawnTrap` Event Functionality**
* **Description:** The `BeatmapEventManager` needs a dedicated method to add `SpawnTrap` events, similar to how `SpawnEnemy` events are handled. This method should encapsulate the specific data pairs required for trap events, including `TrapTypeToSpawn` and optional `TrapHealthInBeats`.
* **Status:** Addressed
* **Resolution/Discussion:** The `add_spawn_trap_event` method was added to `BeatmapEventManager`. It correctly constructs a `SpawnTrap` event dictionary, including dynamic `TrapTypeToSpawn` based on a friendly `trap_type` name lookup, and optionally includes `TrapHealthInBeats`.
* **Reference:** Implemented in `beatmap_event_manager.py` and demonstrated in `main_beatmap_app.py`.

---

**ISSUE 9: Private Path Configuration (Git Ignore)**
* **Description:** Local game installation paths and template file locations should be stored in a separate file that is not committed to version control, enhancing portability and security for different developers or environments.
* **Status:** Addressed
* **Resolution/Discussion:** A new file `game_paths.py` was created to hold these sensitive paths. It was explicitly added to the `.gitignore` file to ensure it's not tracked by Git. All scripts that rely on these paths now import from `game_paths.py`.
* **Reference:** Introduced `game_paths.py` and updated `.gitignore`.

---

**ISSUE 10: Per-Song Folder and Asset Copying for Generated Content**
* **Description:** Each generated custom song should reside in its own dedicated, timestamped folder within the `SONGS_BASE_DIR`. This folder should contain the generated beatmap JSON, the updated `info.json`, and a copy of the audio file template.
* **Status:** Addressed
* **Resolution/Discussion:** The `scripts/generate_zombie_beatmap.py` script was updated to create a new folder using a timestamp and an optional `new_song_name`. It now saves the generated beatmap JSON and the updated `info.json` into this new directory and uses `shutil.copyfile` to copy the audio template into it.
* **Reference:** Implemented in `scripts/generate_zombie_beatmap.py`.

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
        "scripts/parse_lua_to_json.py",
        "main_beatmap_app.py",
        "game_paths_template.py",
        "game_entity_definitions.json",
        "game_trap_definitions.json",
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

{issues_content}

{codebase_content}

## Instructions for AI Assistant

* Always refer to the provided codebase files as the authoritative source for the project's current state.
* When proposing changes, indicate which file(s) are affected and provide clear diffs or updated code blocks.
* Prioritize addressing issues chronologically as listed, or as directed by the user in the current conversation.
* Maintain the established code style and structure.
* Be mindful of the design decisions outlined above.
* Help the user use Conventional Commits and Semantic Versioning.
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