import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique rows, preserving original order.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = []
    seen_rows = []

    # Iterate through rows
    for row in input_grid:
        # Convert row to a list for easier comparison (np.array_equal is slow)
        row_list = row.tolist()
        # Check if the row has been seen before
        if row_list not in seen_rows:
            # Add the row to the output and mark it as seen
            output_grid.append(row_list)
            seen_rows.append(row_list)

    return np.array(output_grid)

# Task examples (replace with actual data)
task_examples = [
    {
        "input": np.array([[1, 2, 3], [4, 5, 6], [1, 2, 3]]),
        "output": np.array([[1, 2, 3], [4, 5, 6]])
    },
    {
        "input": np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        "output": np.array([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
    },
    {
        "input": np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]]),
        "output": np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    },
      {
        "input": np.array([[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]),
        "output": np.array([[5, 5, 5, 5, 5]])
    }
]

# Test the transform function and gather results
results = []
for i, example in enumerate(task_examples):
    transformed_grid = transform(example["input"])
    success = np.array_equal(transformed_grid, example["output"])
    results.append({
        "example": i + 1,
        "success": success,
        "transformed_grid": transformed_grid.tolist(),  # For easy viewing
        "expected_output": example["output"].tolist()
    })

print(results)