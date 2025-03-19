"""
1.  **Find Leftmost and Rightmost Colors:** Scan the input grid to identify the leftmost and rightmost non-zero (non-background) colors.
2.  **Determine Output Height:**
    *   If the bottom row of the `input_grid` contains all zeros, then the `output_grid` height is one less than the `input_grid` height.
    *   Otherwise, the output grid has the same height as the input grid.
3.  **Create Output Grid:** Create a new grid (the output grid) with a width of 2 and the calculated height.
4.  **Populate Output Grid:**
    *   Fill the first column (index 0) of the output grid with the leftmost color found in the input grid.
    *   Fill the second column (index 1) of the output grid with the rightmost color found in the input grid.
5. **Return Output Grid:** Return the created output grid.
"""

import numpy as np

def get_leftmost_non_background_color(grid):
    """Finds the leftmost non-background (non-zero) color in the grid."""
    for x in range(grid.shape[1]):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
    return 0  # Should not be reached for non empty grids

def get_rightmost_non_background_color(grid):
     """Finds the rightmost non-background (non-zero) color in the grid."""
     for x in range(grid.shape[1]-1,-1,-1):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
     return 0

def transform(input_grid):
    # Find the leftmost and rightmost non-background colors
    leftmost_color = get_leftmost_non_background_color(input_grid)
    rightmost_color = get_rightmost_non_background_color(input_grid)

    # Determine the height of original and output grid (same height)
    height = input_grid.shape[0]
    if np.all(input_grid[-1] == 0):
        height -= 1

    # Initialize the output grid with two columns and the determined height
    output_grid = np.zeros((height, 2), dtype=int)

    # Fill the first column with the leftmost color
    output_grid[:, 0] = leftmost_color

    # Fill the second column with the rightmost color
    output_grid[:, 1] = rightmost_color

    return output_grid