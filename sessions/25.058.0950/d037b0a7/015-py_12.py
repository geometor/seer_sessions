import numpy as np

# The provided transform function (for reference)
def transform(input_grid):
    output_grid = np.copy(input_grid)
    for col in range(output_grid.shape[1]):
        if output_grid[1, col] != 0:
            output_grid[2, col] = output_grid[1, col]
    return output_grid

# Example data (replace with actual data from the task)

example_data = [
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 1, 0], [0, 1, 0]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 0, 2], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 0, 2], [0, 0, 2]]),
    },
    {
        "input": np.array([[0, 3, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[0, 3, 0], [0, 3, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[4, 0, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[4, 0, 0], [4, 0, 0], [0, 0, 0]]),
    }

]
# Analyze each example
results = []
for i, example in enumerate(example_data):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    differences = expected_output != actual_output

    results.append(
        {
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "actual_output_shape": actual_output.shape,
            "differences": differences.tolist(),  # Convert to list for easier viewing
            "input_grid": input_grid.tolist(),
            "expected_output": expected_output.tolist(),
            "actual_output": actual_output.tolist()
        }
    )

import json
print(json.dumps(results, indent=2))