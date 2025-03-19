"""
Find the region of interest below a horizontal black dividing line, identify the most frequent non-black color within that region (the "shape"), crop the region to the bounding box of that shape, and finally, recolor the cropped grid, setting all pixels that are not the shape's color to black (0).
"""

import numpy as np
from collections import Counter

def get_region_below_black_line(grid):
    """Finds the region below the horizontal line of 0s."""
    rows, cols = grid.shape
    for r in range(rows):
        if np.all(grid[r, :] == 0):
            return grid[r+1:, :]
    return None  # No black line found

def find_prominent_color(grid):
    """Finds the most frequent non-black color in a grid."""
    counts = Counter(grid.flatten())
    if 0 in counts:
        del counts[0]  # Ignore black
    if not counts:
        return 0 # handle if region is all black
    return counts.most_common(1)[0][0]

def get_bounding_box(grid, color):
    """Finds the bounding box of a color in a grid."""
    rows, cols = grid.shape
    rows_with_color = []
    cols_with_color = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                rows_with_color.append(r)
                cols_with_color.append(c)
    if not rows_with_color: # no bounding box
        return 0,0,0,0

    min_row = min(rows_with_color)
    max_row = max(rows_with_color)
    min_col = min(cols_with_color)
    max_col = max(cols_with_color)
    return min_row, max_row, min_col, max_col

def crop_and_recolor(region, prominent_color):
    """Crops the region to the shape's bounding box and recolors."""
    min_row, max_row, min_col, max_col = get_bounding_box(region, prominent_color)

    if min_row > max_row or min_col > max_col: # handle edge cases
        return np.array([[0]])

    cropped_grid = region[min_row:max_row+1, min_col:max_col+1].copy()

    # Recolor
    rows, cols = cropped_grid.shape
    for r in range(rows):
        for c in range(cols):
            if cropped_grid[r, c] != prominent_color:
                cropped_grid[r, c] = 0
    return cropped_grid

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)

    # 1. Identify Region
    region = get_region_below_black_line(input_grid)
    if region is None:
        return np.array([[0]])

    # 2. Identify Shape (Prominent Color)
    prominent_color = find_prominent_color(region)

    # 3 & 4. Crop and Recolor
    output_grid = crop_and_recolor(region, prominent_color)

    return output_grid.tolist()