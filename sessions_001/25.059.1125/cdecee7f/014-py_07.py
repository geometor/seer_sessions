"""
1.  **Identify Non-Zero Pixels:** Examine the input grid and identify all pixels with a value other than zero.  These pixels constitute the "object" to be copied, regardless of their arrangement.

2.  **Determine Output Dimensions:** Calculate the smallest rectangular region that can encompass *all* identified non-zero pixels. This will define the dimensions of the output grid. Note that this is not just a simple bounding rectangle, it's the minimal rectangle enclosing all non-zero pixels.

3.  **Copy Pixels:** Create an output grid with the calculated dimensions.  Iterate through the *identified non-zero pixels* in the input grid.  For each non-zero pixel, determine its position relative to the top-left corner of the encompassing rectangular region (calculated in step 2). Copy the pixel's value to the corresponding position in the output grid.
"""

import numpy as np

def find_non_zero_pixels(grid):
    # Find the indices of all non-zero elements
    rows, cols = np.where(grid != 0)
    return rows, cols

def calculate_output_dimensions(rows, cols):
    # Calculate the dimensions of the output grid
    if len(rows) == 0:  # Handle the case where there are no non-zero pixels
      return 0, 0
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width, min_row, min_col

def transform(input_grid):
    # Find the indices of all non-zero pixels
    rows, cols = find_non_zero_pixels(input_grid)

    # Calculate output grid dimensions and offset
    height, width, min_row, min_col = calculate_output_dimensions(rows, cols)
    
    # Initialize the output grid with zeros, handling empty case
    output_grid = np.zeros((height, width), dtype=int) if height > 0 and width > 0 else np.array([])

    # Copy non-zero pixels to the output grid, handling empty case
    if height > 0 and width > 0:
        for r, c in zip(rows, cols):
            output_grid[r - min_row, c - min_col] = input_grid[r, c]
            

    return output_grid