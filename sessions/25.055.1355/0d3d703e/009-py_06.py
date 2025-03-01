import numpy as np

def compare_grids(expected_grid, actual_grid):
    """
    Compares two grids and returns the coordinates and values of mismatched pixels.
    Also prints these values.

    Args:
        expected_grid: The expected output grid.
        actual_grid: The actual output grid produced by the transform function.

    Returns:
        A list of tuples, where each tuple contains:
        (row_index, col_index, expected_value, actual_value)
    """
    mismatches = []
    for row_index in range(expected_grid.shape[0]):
        for col_index in range(expected_grid.shape[1]):
            if expected_grid[row_index, col_index] != actual_grid[row_index, col_index]:
                mismatches.append((row_index, col_index, expected_grid[row_index, col_index], actual_grid[row_index, col_index]))
                print(f"Mismatch at ({row_index}, {col_index}): Expected {expected_grid[row_index, col_index]}, Actual {actual_grid[row_index, col_index]}")
    return mismatches

# Example data (replace with actual data from the task)
# Assuming these are read from the JSON, similar to the testing notebook.
train_examples = [
    {
        "input": [[5, 1, 5], [1, 5, 1], [5, 1, 5]],
        "output": [[9, 1, 9], [1, 9, 1], [9, 1, 9]],
    },
     {
        "input": [[1, 8, 8, 8, 1], [1, 8, 5, 8, 1], [1, 8, 8, 8, 1]],
        "output": [[1, 2, 2, 2, 1], [1, 2, 9, 2, 1], [1, 2, 2, 2, 1]],
    },
    {
        "input": [[6, 6, 8, 6, 6], [6, 6, 6, 8, 6], [8, 6, 6, 6, 8], [6, 8, 6, 6, 6], [6, 6, 8, 6, 6]],
        "output": [[0, 0, 2, 0, 0], [0, 0, 0, 2, 0], [2, 0, 0, 0, 2], [0, 2, 0, 0, 0], [0, 0, 2, 0, 0]],
    }
]

def transform(input_grid):

    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate over each cell in the grid
    for row_index in range(output_grid.shape[0]):
        for col_index in range(output_grid.shape[1]):
            # change output pixels by adding 4
            output_grid[row_index, col_index] = output_grid[row_index, col_index] + 4

    return output_grid

for i, example in enumerate(train_examples):
    input_grid = np.array(example["input"])
    expected_output_grid = np.array(example["output"])
    actual_output_grid = transform(input_grid)
    print(f"Train Example {i+1}:")
    compare_grids(expected_output_grid, actual_output_grid)
    print("-" * 20)