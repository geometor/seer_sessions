import json
from collections import defaultdict
from pathlib import Path
from rich.console import Console
from rich.table import Table

def analyze_sessions(sessions_root):
    """
    Analyzes the sessions data to count task runs and check for test matches.

    Args:
        sessions_root: The root directory of the sessions (Path object).

    Returns:
        A list of tuples, sorted by test_match_count, where each tuple contains
        (task_id, run_count, test_match_count).
    """

    task_data = defaultdict(lambda: {"run_count": 0, "test_match_count": 0})

    for session_date_path in sessions_root.iterdir():
        if not session_date_path.is_dir():
            continue

        for task_path in session_date_path.iterdir():
            if not task_path.is_dir():
                continue

            task_id = task_path.name
            task_data[task_id]["run_count"] += 1

            for item in task_path.iterdir():
                if item.name.endswith("test.json"):
                    try:
                        with open(item, "r") as tf:
                            test_json = json.load(tf)
                            for test_row in test_json:
                                if "match" in test_row and test_row.get("match") is True:
                                    task_data[task_id]["test_match_count"] += 1
                                    break  # Only count one match per test file
                    except (json.JSONDecodeError, OSError) as e:
                        print(f"Error processing {item}: {e}")

    # Sort by test_match_count (descending) and then by task_id (ascending)
    sorted_data = sorted(
        task_data.items(),
        key=lambda item: (-item[1]["test_match_count"], item[0])
    )
    return sorted_data

def main():
    scripts_dir = Path(__file__).parent
    sessions_root = scripts_dir.parent / "sessions"
    results = analyze_sessions(sessions_root)

    console = Console()
    table = Table(title="Session Analysis Results")

    table.add_column("Task ID", justify="left", style="cyan")
    table.add_column("Run Count", justify="right", style="magenta")
    table.add_column("Test Match Count", justify="right", style="green")

    for task_id, data in results:
        table.add_row(
            str(task_id),
            str(data["run_count"]),
            str(data["test_match_count"]),
        )

    console.print(table)

if __name__ == "__main__":
    main()

