"""
1.  Locate the Anchor: Find the single red pixel (value 2) within the input grid. This pixel serves as the anchor point for the transformation.
2.  Define the Transformation Region: The transformed region is a rectangular area of blue pixels.
3.  Determine position and dimensions: This region's upper edge is one row above the red pixel, its lower edge one row below the red pixel, its left edge is the column of the red pixel, and its right edge extends one column to the right of the red pixel's column.
4.  Apply the Transformation: Change all the pixels in the transformation region determined in step 3 to blue (value 1). The red pixel remains red.
5.  Background color is ignored: The grid background color does not affect the transformation rule.
"""

import numpy as np
from typing import Tuple, List

def find_pixel_location(grid: np.ndarray, color: int) -> Tuple[int, int] | None:
    """Finds the location of the first pixel of a given color."""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """Transforms the input grid according to the defined rules."""
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Locate the red pixel
    red_pixel_location = find_pixel_location(input_grid, 2)
    if red_pixel_location is None:  # Handle cases where no red pixel exists
        return output_grid

    red_row, red_col = red_pixel_location

    # Define Transformation Region based on red pixel
    start_row = max(0, red_row - 1)
    end_row = min(input_grid.shape[0], red_row + 2)  # +2 because it's non-inclusive
    start_col = red_col # same column as red pixel
    end_col = min(input_grid.shape[1], red_col + 2) # one to the right

    # Apply transformation
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            output_grid[i, j] = 1  # Change to blue

    # Keep red pixel red
    output_grid[red_row, red_col] = 2

    return output_grid