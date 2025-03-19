import numpy as np

def transform_and_compare(input_grid, expected_output_grid):
    """
    Transforms the input grid according to the current rule and compares it with the expected output.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for j in range(cols):
        if input_grid[0, j] != 0:
            for i in range(1, rows):
                output_grid[i, j] = input_grid[0, j]

    comparison = output_grid == expected_output_grid
    print(f"Input:\n{input_grid}\n")
    print(f"Expected Output:\n{expected_output_grid}\n")
    print(f"Actual Output:\n{output_grid}\n")
    print(f"Comparison (True if match, False otherwise):\n{comparison}\n")
    print(f"Overall Match: {np.all(comparison)}\n")
    return np.all(comparison)


# Example usage with the training data (replace with actual data)

# dummy data for demonstration
example_input = np.array([
    [1, 0, 2],
    [0, 0, 0],
    [0, 0, 0]
])

example_output = np.array([
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2]
])

transform_and_compare(example_input, example_output)
