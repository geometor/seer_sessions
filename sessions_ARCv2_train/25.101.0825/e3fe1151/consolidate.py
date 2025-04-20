#!/usr/bin/env python3

import os
import json
import argparse
from pathlib import Path

def read_file_content(file_path, default=""):
    """Safely reads content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return default
    except Exception as e:
        print(f"Warning: Error reading file {file_path}: {e}")
        return default

def format_json_code_block(file_path):
    """Reads a JSON file and formats it as a Markdown code block."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        formatted_json = json.dumps(data, indent=2)
        # Extract filename for the code block tag
        filename = Path(file_path).name
        return f"```json {filename}\n{formatted_json}\n```\n\n"
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return ""
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from file: {file_path}")
        # Attempt to include raw content if JSON parsing fails
        raw_content = read_file_content(file_path)
        filename = Path(file_path).name
        return f"```text {filename} (Invalid JSON)\n{raw_content}\n```\n\n"
    except Exception as e:
        print(f"Warning: Error processing JSON file {file_path}: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser(
        description="Consolidate task session files into a single Markdown file."
    )
    parser.add_argument(
        "task_folder",
        nargs='?',
        default=".",
        help="Path to the task session folder (default: current directory)."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="consolidated_task.md",
        help="Name of the output Markdown file (default: consolidated_task.md)."
    )
    args = parser.parse_args()

    task_path = Path(args.task_folder).resolve()
    output_file_path = task_path / args.output
    markdown_content = []

    print(f"Processing task folder: {task_path}")
    print(f"Output will be saved to: {output_file_path}")

    # 1. Include root index.json
    root_index_path = task_path / "index.json"
    if root_index_path.is_file():
        markdown_content.append(f"# Task Index\n\n")
        markdown_content.append(format_json_code_block(root_index_path))
    else:
        print(f"Warning: Root index.json not found at {root_index_path}")

    # 2. Find and process step folders (numeric names)
    step_folders = sorted(
        [d for d in task_path.iterdir() if d.is_dir() and d.name.isdigit()],
        key=lambda d: int(d.name) # Sort numerically
    )

    if not step_folders:
        print("Warning: No step folders (like '000', '001', ...) found.")

    for step_dir in step_folders:
        step_name = step_dir.name
        print(f"Processing step: {step_name}")

        # Add step heading
        markdown_content.append(f"# {step_name}\n\n")

        # Add step index.json
        step_index_path = step_dir / "index.json"
        if step_index_path.is_file():
            markdown_content.append(format_json_code_block(step_index_path))
        else:
            print(f"Warning: Step index.json not found in {step_dir}")

        # Add prompt_content.md
        prompt_content_path = step_dir / "prompt_content.md"
        if prompt_content_path.is_file():
            markdown_content.append(f"## Prompt Content ({step_name})\n\n")
            markdown_content.append(read_file_content(prompt_content_path) + "\n\n")
        else:
            print(f"Warning: prompt_content.md not found in {step_dir}")


        # Add prompt_instructions.md
        prompt_instructions_path = step_dir / "prompt_instructions.md"
        if prompt_instructions_path.is_file():
            markdown_content.append(f"## Prompt Instructions ({step_name})\n\n")
            markdown_content.append(read_file_content(prompt_instructions_path) + "\n\n")
        else:
            print(f"Warning: prompt_instructions.md not found in {step_dir}")


        # Add response.md
        response_md_path = step_dir / "response.md"
        if response_md_path.is_file():
             markdown_content.append(f"## Response ({step_name})\n\n")
             markdown_content.append(read_file_content(response_md_path) + "\n\n")
        else:
            print(f"Warning: response.md not found in {step_dir}")


        # Add code*.trial.json files
        trial_files = sorted(step_dir.glob("code*.trial.json"))
        if trial_files:
             markdown_content.append(f"## Trial Data ({step_name})\n\n")
             for trial_file in trial_files:
                 markdown_content.append(format_json_code_block(trial_file))
        else:
             print(f"Info: No code*.trial.json files found in {step_dir}")


    # 3. Write the consolidated content to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("".join(markdown_content))
        print(f"\nSuccessfully created consolidated file: {output_file_path}")
    except Exception as e:
        print(f"\nError: Failed to write output file {output_file_path}: {e}")

if __name__ == "__main__":
    main()
