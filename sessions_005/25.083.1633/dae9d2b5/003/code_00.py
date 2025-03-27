"""
1. **Find the Bounding Box:** Examine the input grid and identify the smallest rectangle that contains all non-white pixels (pixels with colors other than 0). This is the bounding box.
2. **Crop:** Create an intermediate grid by cropping the input grid to the dimensions of the bounding box.
3. **Color Substitution:** Iterate through the cropped, intermediate grid.
    *   If a pixel is yellow (4) or green (3), change its color to magenta (6).
    *   If a pixel is white (0), leave it unchanged.
4. The resulting grid is the output grid.
"""

import numpy as np

def get_bounding_box(grid):
    """Find the bounding box of non-white pixels in a grid."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle the case where the grid is all white.
        return None  # No bounding box
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Transforms an input grid by cropping it to the bounding box of non-white pixels
    and replacing yellow (4) and green (3) pixels with magenta (6).
    """
    # Find the bounding box.
    bbox = get_bounding_box(input_grid)

    # Handle the case where the entire grid is white.
    if bbox is None:
        return np.copy(input_grid)

    min_row, min_col, max_row, max_col = bbox

    # Crop the grid.
    cropped_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    # Initialize the output grid with the cropped dimensions.
    output_grid = np.copy(cropped_grid)

    # Perform color substitution.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 4 or output_grid[i, j] == 3:
                output_grid[i, j] = 6

    return output_grid