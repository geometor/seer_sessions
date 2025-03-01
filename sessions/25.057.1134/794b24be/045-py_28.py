import numpy as np

# Example data (replace with actual data from the task)
# Input grids for examples 1 to 3
input_grids = [
    np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]]),  # Example 1 Input
    np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]),  # Example 2 Input
    np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),  # Example 3 Input
]

# Expected output grids for examples 1 to 3
expected_output_grids = [
    np.array([[0, 0, 0], [0, 0, 0], [0, 2, 0]]),  # Example 1 Output
    np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),  # Example 2 Output
    np.array([[0, 2, 0], [0, 2, 0], [0, 2, 0]]),  # Example 3 Output
]
# Transform grids using current function
transformed_grids = []

def get_neighbors(grid, row, col):
    """Get the neighbors of a pixel."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input_grid
    for row in range(rows):
        for col in range(cols):
            # Get the current pixel's color
            current_color = input_grid[row, col]
            # Get the neighboring pixels' colors
            neighbors = get_neighbors(input_grid, row, col)

            # Apply the transformation rules
            if current_color == 1:  # If the pixel is blue
                if 1 in neighbors:  # and any neighbor is blue
                  output_grid[row,col] = 2

            if row == 1 and col == 1: # center pixel
                if input_grid[row, col-1] == 1 and current_color == 0:
                    output_grid[row, col] = 2

            if row == rows - 1:
                if (col == 0 or col == cols -1) and current_color == 1:
                    output_grid[row, col] = 0
    return output_grid

for grid in input_grids:
  transformed_grids.append(transform(grid))

# Compare transformed grids with expected outputs
comparison_results = []
for i in range(len(expected_output_grids)):
    comparison = transformed_grids[i] == expected_output_grids[i]
    comparison_results.append(comparison)
    print(f"Example {i+1} Comparison (Transformed == Expected):\n{comparison}\n")
    print(f"Number of mismatches: {np.sum(~comparison)}")
