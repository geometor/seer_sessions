"""
1.  **Identify Blue Region:** Locate all blue (1) pixels in the input grid.
2.  **Extract Region:** Create the smallest possible output grid that fits the blue area.
3.  **Recolor:** Inside the output grid, change all blue pixels to gray (5). All other pixels in this region are black.
4.  **Output:** present the transformed output.
"""

import numpy as np

def get_blue_region(grid):
    """Finds the coordinates of all blue pixels."""
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:
        return None
    return rows, cols

def transform(input_grid):
    # Find coordinates of blue pixels
    blue_region = get_blue_region(input_grid)

    # Handle the case where there are no blue pixels
    if blue_region is None:
        return np.zeros((1, 1), dtype=int)

    rows, cols = blue_region

    # Determine the dimensions of the output grid
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    
    # Initialize the output grid with all zeros (black)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Recolor the blue pixels to gray (5) within the output grid
    for i in range(len(rows)):
        output_row = rows[i] - min_row
        output_col = cols[i] - min_col
        output_grid[output_row, output_col] = 5

    return output_grid