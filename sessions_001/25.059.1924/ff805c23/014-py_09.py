"""
1. **Identify the Outer Boundary:** Find the outermost rectangle formed by magenta (color 6) pixels.

2. **Find the Inner Bounding Box** Identify an inner rectangular region, within the outer magenta boundary, based on the non-magenta pixels within. The top, bottom, left, and right sides should align directly inside the magenta border.

3. **Create Output Grid:** Create a new grid filled with magenta (color 6) pixels, with dimensions matching the inner bounding box.

4. **Copy Exception Pixels:** Copy any white (color 0) pixels from their corresponding locations within the inner bounding box in the *input* grid to the *output* grid.
"""

import numpy as np

def find_bounding_box(grid, color):
    """Finds the bounding box of a given color."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def find_inner_bounding_box(grid):
    """
    Finds the inner bounding box defined by the region of interest (ROI)
    within the area bounded by magenta (color 6).
    """
    rows, cols = grid.shape
    
    # Find outermost magenta pixels
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = find_bounding_box(grid, 6)

    # Find top boundary of ROI (looking downwards from the outermost top magenta)
    top_row = outer_min_row + 1

    # Find bottom boundary of ROI (looking upwards from the outermost bottom magenta)
    bottom_row = outer_max_row - 1

    # Find left boundary of ROI (looking rightwards from the outermost left magenta)
    left_col = outer_min_col + 1
    
    # Find right boundary of ROI (looking leftwards from the outermost right magenta)
    right_col = outer_max_col - 1
        
    return top_row, left_col, bottom_row, right_col

def transform(input_grid):
    # Find the outer boundary (magenta).
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = find_bounding_box(input_grid, 6)

    # Find the inner bounding box (ROI).
    top_row, left_col, bottom_row, right_col = find_inner_bounding_box(input_grid)

    # Calculate height and width of the ROI.
    height = bottom_row - top_row + 3
    width = right_col - left_col + 3

    # Initialize output grid with the calculated dimensions, filled with 6s.
    output_grid = np.full((height, width), 6, dtype=int)

    # Copy color 0 pixels from the input ROI to the output grid.
    for r in range(height):
        for c in range(width):
            input_row = top_row + r -1
            input_col = left_col + c -1
            if 0 <= input_row < input_grid.shape[0] and 0 <= input_col < input_grid.shape[1] and input_grid[input_row, input_col] == 0:
                output_grid[r, c] = input_grid[input_row, input_col]

    return output_grid