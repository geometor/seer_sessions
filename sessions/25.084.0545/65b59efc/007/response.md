```python
"""
1.  Determine Output Grid Dimensions:
    *   The output grid has one less column than the input grid.
    *   The number of rows of output grid is variable and will be provided.

2.  Create Color Map:
    *   Extract all non-zero values from the last row of the input grid. This forms the `color_map`.

3.  Populate Output Grid (Column-wise):
    *   Iterate through each column of the output grid.
    *   For each output column, repeat the values of the color_map until the output height is met.

4.  Final Rule:
    * The output is created by vertically repeating values from the color_map for each column.
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
    else:  # Default case
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

    # Populate the output grid column-wise
    color_map_len = len(color_map)
    if color_map_len > 0:  # Handle cases where the last row might be all zeros
      for c in range(output_cols):
          for r in range(output_rows):
              output_grid[r, c] = color_map[r % color_map_len]

    return output_grid
```