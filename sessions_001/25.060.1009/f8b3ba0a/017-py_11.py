import numpy as np

def get_non_white_rows(grid):
    """Returns rows that aren't all white (0)."""
    grid_np = np.array(grid)
    non_white_rows = []
    for row in grid_np:
        if not np.all(row == 0):
            non_white_rows.append(row)
    return non_white_rows

def test_examples(task):
    """Tests all examples and reports differences."""
    correct_count = 0
    for example in task["train"]:
        input_grid = example["input"]
        expected_output = example["output"]
        predicted_output = get_non_white_rows(input_grid)
        if np.array_equal(np.array(predicted_output), np.array(expected_output)):
            correct_count += 1
            print(f"Example: PASSED")
        else:
            print(f"Example: FAILED")
            print(f"  Input:\n{np.array(input_grid)}")
            print(f"  Expected Output:\n{np.array(expected_output)}")
            print(f"  Predicted Output:\n{np.array(predicted_output)}")
            print("-" * 20)
    print(f"Total correct {correct_count} out of {len(task['train'])}.")

# get the current task from the environment
import json
import os
task_file = os.environ.get('TASK')
task = json.load(open(task_file, 'r'))

test_examples(task)