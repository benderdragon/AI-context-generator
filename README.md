# AI Project Context Generator

A simple, dependency-free Python script that consolidates project documentation and source code into a single, prompt-friendly Markdown file. This tool is designed to make it easy to provide a large amount of context to Large Language Models (LLMs) like GPT, Claude, and others.

## Key Features

- **Consolidates Everything:** Merges key documentation files (`README.md`, instructions, issues, etc.) and your entire codebase into one file.
- **Intelligent Filtering:**
    - Respects your project's `.gitignore` rules.
    - Allows for fine-grained, explicit exclusion of files and folders that might be in source control but are irrelevant for an AI assistant (e.g., `package-lock.json`).
- **Handles Large Projects:** Automatically splits the output into multiple numbered parts if the total size exceeds a configurable character limit, preventing prompt overloads.
- **Zero Dependencies:** Requires only a standard Python installation to run.
- **Highly Configurable:** All options are managed in a simple, project-specific runner script, keeping the core logic clean and portable.

## Setup & Installation

To use this generator in your project:

1.  Create a `scripts/` directory in your project's root folder if it doesn't already exist.
2.  Copy the following two files into your `scripts/` directory:
    - `generate_context_markdown.py` (The core logic)
    - `run_context_generator.py` (The project-specific configuration)

Your project structure should look something like this:

```
my_project/
├── .git/
├── .gitignore
├── docs/
│   └── ai_instructions.md
├── scripts/
│   ├── generate_context_markdown.py
│   └── run_context_generator.py
├── src/
│   └── ...
└── README.md
```

## Usage

1.  **Configure:** Open `scripts/run_context_generator.py` and edit the configuration variables at the top of the file to match your project's needs. See the **Configuration Options** section below for details.
2.  **Run:** Execute the runner script from your project's **root directory**:
    ```bash
    python scripts/run_context_generator.py
    ```
3.  **Use:** The generated context file(s) will be created in an `output/` directory. Copy and paste the entire content of the file (or all parts, in order) into your AI assistant's prompt.

---

## Configuration Options

All configuration is done in `scripts/run_context_generator.py`.

| Variable                      | Type          | Description                                                                                                                                                             |
| ----------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PROJECT_NAME`                | `str`         | The name of your project, which will be used in the titles of the generated context file.                                                                               |
| `OPTIONAL_DOCS_TO_INCLUDE`    | `List[str]`   | A list of specific documentation files to include in the context preamble. Paths are relative to the project root.                                                      |
| `DOC_FOLDERS_TO_SCAN`         | `List[str]`   | A list of folders to scan recursively for any `.md` files, which will all be included in the preamble. Useful for directories with auto-generated documentation.        |
| `FILES_TO_EXCLUDE`            | `List[str]`   | A list of specific file names or paths to explicitly exclude from the context. Perfect for files like `package-lock.json`.                                              |
| `FOLDERS_TO_EXCLUDE`          | `List[str]`   | A list of folder names or paths to explicitly exclude. Any folder listed here will not be scanned. The default list includes common folders like `.git`, `node_modules`, etc. |
| `MAX_CHARACTERS`              | `int`         | The maximum approximate character limit for a single output file. If the context exceeds this, it will be split.                                                        |
| `SPLIT_FILES`                 | `bool`        | If `True`, the output will be split into multiple parts when `MAX_CHARACTERS` is exceeded. If `False`, the output will simply be truncated.                               |

### How It Works

The script performs the following steps:
1.  **Gathers a Preamble:** It reads the main `README.md`, `ai_instructions.md`, and any files/folders specified in `OPTIONAL_DOCS_TO_INCLUDE` and `DOC_FOLDERS_TO_SCAN`. This forms the introductory part of the context.
2.  **Scans the Codebase:** It walks through your project directory to find all files.
3.  **Applies Filters:** It ignores files and directories based on a set of rules, in the following order:
    1.  Itself and its own output files.
    2.  Any files that were already included in the preamble.
    3.  Anything listed in the `FILES_TO_EXCLUDE` and `FOLDERS_TO_EXCLUDE` configuration.
    4.  Anything matching a pattern in your root `.gitignore` file.
4.  **Generates Output:** It combines the preamble and the content of all filtered files into a single Markdown file, splitting it into parts if necessary.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.