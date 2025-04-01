#!/usr/bin/env python3

import sys
from pathlib import Path
from collections import defaultdict
from rich.console import Console
from rich.table import Table

def find_duplicate_tasks(corpus_dirs: list[Path]) -> dict[str, list[str]]:
    """
    Scans specified corpus directories for task files (*.json) and identifies
    task IDs present in more than one directory.

    Args:
        corpus_dirs: A list of Path objects representing the directories to scan.

    Returns:
        A dictionary where keys are task IDs found in multiple corpora,
        and values are lists of the names of the corpora containing that task ID.
        Returns an empty dictionary if no duplicates are found.
    """
    task_locations = defaultdict(list)
    valid_corpus_names = []

    print("Scanning directories...")
    for corpus_dir in corpus_dirs:
        # Ensure we are working with Path objects
        corpus_path = Path(corpus_dir)
        if not corpus_path.is_dir():
            print(f"Warning: '{corpus_path}' is not a valid directory. Skipping.", file=sys.stderr)
            continue

        corpus_name = corpus_path.parent.name + '_' + corpus_path.name # Use the directory name as the corpus identifier
        valid_corpus_names.append(corpus_name)
        print(f" -> Scanning '{corpus_name}' ({corpus_path})...")
        found_count = 0
        for task_file in corpus_path.glob('*.json'):
            if task_file.is_file():
                task_id = task_file.stem  # Get filename without extension
                task_locations[task_id].append(corpus_name)
                found_count += 1
        print(f"    Found {found_count} task files.")

    print("\nIdentifying duplicates...")
    duplicates = {}
    for task_id, locations in task_locations.items():
        # Use set to count unique corpus names for a task_id
        if len(set(locations)) > 1:
            duplicates[task_id] = sorted(list(set(locations))) # Store unique, sorted list

    return duplicates

def main():
    # --- Define your corpus directories here ---
    # Replace these example paths with the actual paths to your corpus folders
    corpus_directory_paths = [
        "../tasks/ARCv1/training",
        "../tasks/ARCv1/evaluation",
        "../tasks/ARCv2/training",
        "../tasks/ARCv2/evaluation",
    ]
    # -------------------------------------------

    # Convert string paths to Path objects and resolve them (optional but good practice)
    absolute_corpus_dirs = [Path(p).resolve() for p in corpus_directory_paths]

    duplicate_tasks = find_duplicate_tasks(absolute_corpus_dirs)

    if not duplicate_tasks:
        print("\nNo duplicate task IDs found across the specified directories.")
    else:
        print(f"\nFound {len(duplicate_tasks)} duplicate task IDs:")

        # --- Create and print the rich table ---
        console = Console()
        table = Table(title="Duplicate Task IDs Across Corpora", show_header=True, header_style="bold magenta")

        # Determine all unique corpus locations involved in duplicates
        all_locations = set()
        for locations in duplicate_tasks.values():
            all_locations.update(locations)
        #  all_locations = sorted(list(all_locations))

        # Add columns to the table
        table.add_column("Task ID", style="dim", width=12)
        for loc in all_locations:
            table.add_column(loc, justify="center")

        # Add rows to the table
        # Sort by task ID for consistent output
        for task_id in sorted(duplicate_tasks.keys()):
            locations = duplicate_tasks[task_id]
            row_data = [task_id]
            for loc_header in all_locations:
                if loc_header in locations:
                    row_data.append("[green]X[/]") # Mark if found
                else:
                    row_data.append("") # Empty if not found
            table.add_row(*row_data)

        console.print(table)

if __name__ == "__main__":
    main()
