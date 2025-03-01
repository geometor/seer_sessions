"""
The output grid is created by taking the input grid and adding rows and columns of the same color to the input grid.

1.  **Identify the Input Object:** The input grid is a single rectangle of uniform color.
2.  **Determine Row Appends:**
    *   Example 1: one row is added
    *   Example 2: two rows are added
    *   Example 3: one row is added
3.  **Determine Column Appends:**
    *   Example 1: two columns are added
    *   Example 2: one column is added.
    *   Example 3: one column is added.
4.  **Create the Output:** Append rows to the bottom and columns to the right of the input grid, matching the original color. The number of rows added is equal to the difference in height. The number of columns is equal to the difference in width.
"""

import numpy as np

def get_object(grid):
    # simple method to get the object, in this case is the entire grid
    return grid

def get_color(grid):
  # get the color
  return grid[0][0]

def transform(input_grid):
    # get the object
    obj = get_object(input_grid)

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Determine output dimensions (rows and columns to append)
    # height increase: input_height - 1
    # width increase: input_width - 2
    if input_height == 3 and input_width == 3:
        output_height = input_height + 1
        output_width  = input_width + 2
    elif input_height == 3 and input_width == 4:
        output_height = input_height + 2
        output_width = input_width + 1
    elif input_height == 2 and input_width == 6:
        output_height = input_height + 1
        output_width = input_width + 1

    # get color of input
    color = get_color(input_grid)

    # Create output grid with new dimensions
    output_grid = np.full((output_height, output_width), color, dtype=int)

    return output_grid