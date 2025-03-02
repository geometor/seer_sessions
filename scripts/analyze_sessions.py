import json
from collections import defaultdict
from pathlib import Path
from rich.console import Console
from rich.table import Table
import shutil  # Import shutil for file copying

def analyze_sessions(sessions_root):
    """
    Analyzes the sessions data, counts task runs, checks for test matches,
    and generates reports.

    Args:
        sessions_root: The root directory of the sessions (Path object).

    Returns:
        A list of tuples, sorted by test_match_count, where each tuple contains
        (task_id, run_count, test_match_count).
    """

    task_data = defaultdict(lambda: {"run_count": 0, "test_match_count": 0})
    reports_root = Path("../reports") #added for use later

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

                                    # --- Report Generation (Solved) ---
                                    report_dir = reports_root / "solved" / task_id / session_date_path.name
                                    report_dir.mkdir(parents=True, exist_ok=True)

                                    # Find prefix:  "008-py_06-test.json" -> "008-"
                                    prefix = item.name.split("-")[0] + "-"
                                    # Copy matching files
                                    for file_to_copy in task_path.glob(f"{prefix}*"):
                                        shutil.copy(file_to_copy, report_dir / file_to_copy.name)

                                    break  # Only count/copy one match per test file
                                elif "match" in test_row and test_row.get("match") is False:
                                     # --- Report Generation (Failed) ---
                                    report_dir = reports_root / "test_failed" / task_id / session_date_path.name
                                    report_dir.mkdir(parents=True, exist_ok=True)
                                    prefix = item.name.split("-")[0] + "-"
                                    # Copy matching files
                                    for file_to_copy in task_path.glob(f"{prefix}*"):
                                        shutil.copy(file_to_copy, report_dir / file_to_copy.name)


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

    # Main Results Table
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

    # Summary Table
    total_unique_tasks = len(results)
    total_tasks_with_matches = sum(1 for _, data in results if data["test_match_count"] > 0)
    if total_unique_tasks > 0:
        percent_solved = (total_tasks_with_matches / total_unique_tasks) * 100
    else:
        percent_solved = 0.00

    summary_table = Table(title="Summary")
    summary_table.add_column("Metric", justify="left", style="cyan")
    summary_table.add_column("Value", justify="right", style="magenta")
    summary_table.add_row("Total Unique Tasks", str(total_unique_tasks))
    summary_table.add_row("Tasks with Test Matches", str(total_tasks_with_matches))
    summary_table.add_row("Percent Solved", f"{percent_solved:.2f}%")
    console.print(summary_table)

if __name__ == "__main__":
    main()
