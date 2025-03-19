import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_shape = predicted_grid.shape if predicted_grid is not None else (0,0)
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    predicted_colors = np.unique(predicted_grid) if predicted_grid is not None else []
    print(f"  Input shape: {input_shape}, Colors: {input_colors}")
    print(f"  Output shape: {output_shape}, Colors: {output_colors}")
    print(f"  Predicted shape: {predicted_shape}, Colors: {predicted_colors}")
    print(f"  Correct Prediction?: {np.array_equal(output_grid, predicted_grid)}")

# Example grids from the training set
examples = [
    (np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]]), np.array([[3, 0, 3], [0, 0, 0], [3, 0, 3]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]), np.array([[3, 0, 0, 3], [0, 0, 0, 0], [0, 0, 0, 0], [3, 0, 0, 3]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]), np.array([[3, 0, 0, 0, 3], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [3, 0, 0, 0, 3]])),
]

# Simulate previous transform function
def transform(input_grid):
    # Find the first non-zero color and its location
    def get_first_nonzero_color_and_location(grid):
      # Iterate through the grid to find the first non-zero color
      rows, cols = grid.shape
      for r in range(rows):
          for c in range(cols):
              if grid[r, c] != 0:
                  return grid[r, c], (r,c)
      return 0, (0,0)  # Return default if no non-zero color is found

    def get_dimensions(input_grid, first_non_zero_loc):
        # use location of first non-zero to determine height
        h = first_non_zero_loc[0]
        return h+1

    first_nonzero_color, first_nonzero_location = get_first_nonzero_color_and_location(input_grid)

    # determine the dimensions of output grid
    h = get_dimensions(input_grid, first_nonzero_location)

    # Initialize output_grid with all zeros (white)
    output_grid = np.zeros((h, h), dtype=int)

    # Populate corners of the output_grid with green (3) based off the input
    output_grid[0, 0] = 3
    output_grid[0, -1] = 3
    output_grid[-1, 0] = 3
    output_grid[-1, -1] = 3

    return output_grid

# Run analysis and transform for each example

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    predicted_grid = transform(input_grid)
    analyze_example(input_grid, output_grid, predicted_grid)
    print("-" * 20)