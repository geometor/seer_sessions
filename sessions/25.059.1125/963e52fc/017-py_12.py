import numpy as np

def describe_grid(grid):
    """Provides a concise description of a grid."""
    return f"Shape: {grid.shape}, Colors: {np.unique(grid)}"

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    """Analyzes a single example and its results."""
    print("Input Grid:", describe_grid(input_grid))
    print("Expected Output Grid:", describe_grid(expected_output_grid))
    print("Predicted Output Grid:", describe_grid(predicted_output_grid))

    match = np.array_equal(expected_output_grid, predicted_output_grid)
    print("Match:", match)

    if not match:
        print("Differences:")
        diff = expected_output_grid != predicted_output_grid
        print(diff)



# Example Data (replace with actual data from the task)
examples = [
    (
        np.array([[0, 0, 0], [1, 2, 1], [0, 0, 0]]),  # Example 1 Input
        np.array([[0, 0, 0, 0, 0, 0], [1, 2, 1, 1, 2, 1], [0, 0, 0, 0, 0, 0]]),  # Example 1 Expected Output
    ),
      (
        np.array([[0, 0, 0, 0], [1, 2, 1, 2], [0, 0, 0, 0]]),  # Example 2 Input
        np.array([[0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 1, 2, 1, 2, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0]]),  # Example 2 Expected Output
    ),
     (
        np.array([[0, 0, 0, 0, 0], [1, 2, 1, 2, 1], [0, 0, 0, 0, 0]]),  # Example 3 Input
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 1, 2, 1, 1, 2, 1, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),  # Example 3 Expected Output
    )
]

# transform function (from previous code)
def transform(input_grid):
    # Initialize output_grid with doubled width, same height, and filled with 0s.
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Iterate through each row of the input grid.
    for i in range(input_grid.shape[0]):
        # Check if the row contains the pattern (1s and 2s).
        if 1 in input_grid[i] or 2 in input_grid[i]:
            # Double the pattern horizontally.
            new_row = np.concatenate((input_grid[i], input_grid[i]))
            output_grid[i] = new_row
        else:
            # expand the row by adding 0
            output_grid[i] = np.concatenate((input_grid[i], input_grid[i]))

    return output_grid

for i, (input_grid, expected_output_grid) in enumerate(examples):
    predicted_output_grid = transform(input_grid)
    print(f"\nExample {i+1}:")
    analyze_example(input_grid, expected_output_grid, predicted_output_grid)