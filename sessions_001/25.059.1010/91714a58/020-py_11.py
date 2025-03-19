"""
Identifies the single rectangular object in the input grid and reproduces it in the output grid, setting all other pixels to 0.
"""

import numpy as np

def find_rectangle(grid):
    """
    Finds the bounding box of a single rectangle in the grid.
    Assumes there's only one rectangle.
    """
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1
    color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                color = grid[r,c]
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if max_row == -1:  # No rectangle found
        return None, None, None

    return (min_row, min_col, max_row, max_col), color


def transform(input_grid):
    # Initialize output_grid with all zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find the rectangle's bounding box and color
    rectangle_bbox, color = find_rectangle(input_grid)

    if rectangle_bbox is not None:
        min_row, min_col, max_row, max_col = rectangle_bbox

        # Reconstruct the rectangle in the output grid
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                output_grid[r, c] = color

    return output_grid