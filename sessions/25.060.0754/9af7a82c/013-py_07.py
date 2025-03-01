import numpy as np

def compare_grids(expected, actual):
    if expected.shape != actual.shape:
        return f"Shape mismatch: Expected {expected.shape}, Actual {actual.shape}"
    diff = expected != actual
    if not np.any(diff):
        return "Grids are identical."
    diff_indices = np.where(diff)
    num_differences = len(diff_indices[0])
    first_diff = (diff_indices[0][0], diff_indices[1][0])
    return f"Grids differ. Number of differences: {num_differences}, First difference at: {first_diff}"

# Example data - Placeholder, replace with actual from test run
task_examples = [
    {
        "input": np.array([[1, 2, 3], [4, 5, 6]]),
        "expected": np.array([[0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 5, 6], [4, 5, 6]]),
        "name": "Example 1"

    },
    {
        "input": np.array([[7, 8, 9, 1], [2, 3, 4, 5]]),
        "expected": np.array([[0, 9, 8, 7], [0, 4, 3, 2], [0, 4, 3, 2], [0, 4, 3, 2], [0, 4, 3, 2], [2, 3, 4, 5]]),
        "name": "Example 2"
    },
      {
        "input": np.array([[7, 8, 9, 1, 4, 5], [2, 3, 4, 5, 7, 8]]),
        "expected": np.array([[5, 4, 1, 9, 8, 7], [8, 7, 5, 4, 3, 2]]),
        "name": "Example 3"
    }
]
results = []
for ex in task_examples:
   input_grid = ex["input"]
   expected_grid = ex['expected']
   actual_grid = transform(input_grid)
   comparison_result = compare_grids(expected_grid, actual_grid)
   results.append(f"{ex['name']}: {comparison_result}")

for r in results:
    print(r)
