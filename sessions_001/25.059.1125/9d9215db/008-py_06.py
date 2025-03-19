"""
1. Preserve Red Pixels: Identify and preserve the position of any red pixels. These remain unchanged in the output.

2. Azure to Column of Blue: Identify the x-coordinate (column) where the azure pixel exists. Extend a blue vertical line on this x-coordinate in the entire grid, covering the whole column.

3. Azure to Azure, Column Shifted:
    - Identify all azure-colored pixels or rectangles in the input.
    - For each azure object, create a single azure pixel in the output.
    - The output azure pixel's row is kept.
    - Find the column that has the vertical blue line. The new azure pixel column is this value.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of pixels of the specified color."""
    return list(zip(*np.where(grid == color)))

def transform(input_grid):
    """Transforms the input grid according to the identified rules."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Preserve Red Pixels
    red_pixels = find_pixels_by_color(input_grid, 2)
    for r, c in red_pixels:
        output_grid[r, c] = 2

    # 2. Find Azure and Create Blue Column
    azure_pixels = find_pixels_by_color(input_grid, 8)
    blue_column = -1
    if azure_pixels:  # Check if any azure pixels exist
      # Use the column of *first* azure pixel (if multiple exist)
      first_azure_col = azure_pixels[0][1]
      for r in range(rows):
            output_grid[r, first_azure_col] = 1
      blue_column = first_azure_col

    # 3. Azure to Azure, Column Shifted
    for r, c in azure_pixels:
        if blue_column != -1: #only if exists
          output_grid[r, blue_column] = 8


    return output_grid