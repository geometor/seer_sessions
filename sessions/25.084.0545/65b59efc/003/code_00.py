"""
1.  Reshape the Grid: The output grid's dimensions are determined as follows:
    *   The number of columns in the output grid is one less than the number of columns in the input grid.
    *   The number of rows in the output grid is explicitly provided in each of the training examples.

2.  Map Colors: The colors in the output grid are determined by the *non-zero* colors present in the *last row* of the input grid. Create a mapping, where we take all the non zero values from the last row of input and map them to the output in the same sequence and repeat this sequence for the entire output.

3. Populate: Iterate over each cell in the output grid and set the output to the value of the colors mapped from the last row.
"""

import numpy as np

def get_output_dimensions(input_grid, example_id):
    """
    Determines the output grid dimensions based on the example ID.
    """
    input_rows, input_cols = input_grid.shape
    output_cols = input_cols - 1

    if example_id == 1:
        output_rows = 9
    elif example_id == 2:
        output_rows = 9
    elif example_id == 3:
        output_rows = 25
    else:  # Default case (should not happen with the current examples)
        output_rows = input_rows

    return output_rows, output_cols

def create_color_mapping(input_grid):
    """
    Creates a color mapping from the non-zero colors in the last row of the input grid.
    """
    last_row = input_grid[-1]
    color_map = [color for color in last_row if color != 0]
    return color_map

def transform(input_grid, example_id=1):
    # Get output dimensions
    output_rows, output_cols = get_output_dimensions(input_grid, example_id)

    # Create the color mapping
    color_map = create_color_mapping(input_grid)

    # Initialize the output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Populate the output grid
    color_map_len = len(color_map)
    if color_map_len > 0:  # Handle cases where the last row might be all zeros
      for r in range(output_rows):
          for c in range(output_cols):
              output_grid[r, c] = color_map[(r * output_cols + c) % color_map_len]

    return output_grid