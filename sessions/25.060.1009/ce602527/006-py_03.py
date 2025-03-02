"""
Transforms a larger grid into a 5x5 grid, representing a simplified version of a red square with a blue "pixel" found in the input. The output is always 5x5, filled with red, with a single blue pixel representing the relative position of the blue pixel within the red square in the input.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous region of the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid into a 5x5 abstracted representation."""

    # Initialize a 5x5 output grid filled with red (2).
    output_grid = np.full((5, 5), 2, dtype=int)

    # Find the bounding box of the red object.
    red_bbox = find_object(input_grid, 2)
    if red_bbox is None:
        return output_grid  # No red object found, return all-red grid

    # Find the bounding box of the blue object.
    blue_bbox = find_object(input_grid, 1)
    if blue_bbox is None:
        return output_grid  # No blue object found, return all-red grid
    
    # Get coordinates
    red_min_row, red_min_col = red_bbox[0]
    red_max_row, red_max_col = red_bbox[1]
    blue_min_row, blue_min_col = blue_bbox[0]
    
    #calculate relative position
    row_rel = (blue_min_row - red_min_row) / (red_max_row - red_min_row) if (red_max_row - red_min_row) > 0 else 0
    col_rel = (blue_min_col - red_min_col) / (red_max_col- red_min_col) if (red_max_col- red_min_col) > 0 else 0

    # Map relative positions to output grid indices (0-4).
    output_row = int(row_rel * 4)  # Scale to 0-4 range
    output_col = int(col_rel * 4)  # Scale to 0-4 range

    # Place the blue pixel.
    output_grid[output_row, output_col] = 1

    return output_grid