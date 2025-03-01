import numpy as np

def describe_grid(grid):
    """Provides a basic description of a grid."""
    height, width = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}
    return f"Dimensions: {height}x{width}, Colors: {unique_colors}, Counts: {color_counts}"

# Example Data (replace with actual data from the task)
example_inputs = [
    np.array([[0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]),
    np.array([[0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]),
    np.array([[0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0],
              [0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 4, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0]]),
]

example_outputs = [
    np.array([[0, 4, 4, 4],
              [4, 9, 4, 4],
              [4, 9, 4, 4],
              [1, 4, 4, 4]]),
    np.array([[0, 4, 4, 4],
              [4, 9, 4, 4],
              [4, 4, 4, 4],
              [4, 4, 4, 4]]),
    np.array([[0, 4, 4, 4],
              [4, 4, 4, 4],
              [4, 4, 4, 4],
              [1, 4, 4, 4]]),
    np.array([[0, 4, 4, 4],
             [4, 4, 4, 4],
             [4, 9, 4, 4],
             [1, 4, 4, 4]]),
    np.array([[0, 4, 4, 4],
             [4, 9, 4, 4],
             [4, 4, 4, 4],
             [1, 4, 4, 4]]),
]
def transform(input_grid):
    # Initialize the output grid as a 4x4 array filled with yellow (4).
    output_grid = np.full((4, 4), 4, dtype=int)

    # Extract relevant pixels from the input grid
    # From 4th column: all yellow (4) - already in output
    # From 9th column: elements at 2nd and 3rd row which are maroon (9)
    # From 13th column: element at the 4th row which is blue(1)
    
    if input_grid.shape[1] >= 9: #making sure we do not go out of bound
       output_grid[1, 1] = input_grid[1, 8]  # 2nd row, 9th column (index 8)
       output_grid[2, 1] = input_grid[2, 8]  # 3rd row, 9th column (index 8)

    if input_grid.shape[1] >=13:
        output_grid[3, 0] = input_grid[3, 12]  # 4th row, 13th column (index 12)

    output_grid[0,0] = 0
    
    return output_grid

for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print("Input Grid Description:", describe_grid(input_grid))
    print("Expected Output Description:", describe_grid(expected_output))
    print("Predicted Output Description:", describe_grid(predicted_output))
    print("Match:", np.array_equal(predicted_output, expected_output))
    print("-" * 20)
