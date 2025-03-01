import json
from collections import defaultdict
from pathlib import Path

def analyze_sessions(sessions_root):
    """
    Analyzes the sessions data to count task runs and check for test matches.

    Args:
        sessions_root: The root directory of the sessions (Path object).

    Returns:
        A dictionary where keys are task IDs and values are dictionaries
        containing 'run_count' and 'test_match_count'.
    """

    task_data = defaultdict(lambda: {"run_count": 0, "test_match_count": 0})

    for session_date_path in sessions_root.iterdir():
        if not session_date_path.is_dir():
            continue

        for session_path in session_date_path.iterdir():
            if not session_path.is_dir():
                continue

            task_json_path = session_path / "task.json"
            if task_json_path.exists():
                try:
                    with open(task_json_path, 'r') as f:
                        task_json = json.load(f)
                        task_id = task_json.get("task_id")

                    if task_id:
                        task_data[task_id]["run_count"] += 1

                        # Check for test files
                        for item in session_path.iterdir():
                            if item.name.endswith("-test.json"):
                                with open(item, "r") as tf:
                                    test_data = json.load(tf)
                                    if test_data.get("match") is True:  # More explicit check
                                        task_data[task_id]["test_match_count"] += 1
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Error processing {task_json_path}: {e}")
                    continue  # Keep going

    return task_data

def main():
    # Construct the path to the sessions directory (sibling of scripts)
    scripts_dir = Path(__file__).parent  # Path to the 'scripts' directory
    sessions_root = scripts_dir.parent / "sessions"

    results = analyze_sessions(sessions_root)

    for task_id, data in results.items():
        print(f"Task ID: {task_id}")
        print(f"  Run Count: {data['run_count']}")
        print(f"  Test Match Count: {data['test_match_count']}")
        print("-" * 20)

if __name__ == "__main__":
    main()
