import os
import json
from collections import defaultdict

def analyze_sessions(sessions_root):
    """
    Analyzes the sessions data to count task runs and check for test matches.

    Args:
        sessions_root: The root directory of the sessions.

    Returns:
        A dictionary where keys are task IDs and values are dictionaries
        containing 'run_count' and 'test_match_count'.
    """

    task_data = defaultdict(lambda: {"run_count": 0, "test_match_count": 0})

    for session_date in os.listdir(sessions_root):
        session_date_path = os.path.join(sessions_root, session_date)
        if not os.path.isdir(session_date_path):
            continue

        for session_id in os.listdir(session_date_path):
            session_path = os.path.join(session_date_path, session_id)
            if not os.path.isdir(session_path):
                continue

            task_json_path = os.path.join(session_path, "task.json")
            if os.path.exists(task_json_path):
                try:
                    with open(task_json_path, 'r') as f:
                        task_json = json.load(f)
                        task_id = task_json.get("task_id")  # Use .get() for safety

                    if task_id:
                        task_data[task_id]["run_count"] += 1

                        #check for test files
                        for file in os.listdir(session_path):
                            if file.endswith("-test.json"):
                                test_file = os.path.join(session_path,file)
                                with open(test_file, "r") as tf:
                                    test_data = json.load(tf)
                                    if test_data.get("match") == True:
                                        task_data[task_id]["test_match_count"] += 1
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Error processing {task_json_path}: {e}")
                    continue #keep going

    return task_data

def main():
    sessions_root = "../sessions"  # Assuming 'sessions' is in the current directory.
    results = analyze_sessions(sessions_root)

    for task_id, data in results.items():
        print(f"Task ID: {task_id}")
        print(f"  Run Count: {data['run_count']}")
        print(f"  Test Match Count: {data['test_match_count']}")
        print("-" * 20)

if __name__ == "__main__":
    main()
