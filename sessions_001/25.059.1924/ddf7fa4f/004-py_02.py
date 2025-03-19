"""
The transformation rule involves identifying specific colors in the top row of the input grid (excluding white/0) and using them to replace a contiguous gray (5) region. The gray region is replaced from left to right and top to bottom with rectangular-like regions of the identified colors. The colors used are red (2), magenta (6), and azure (8). The rest of the grid remains unchanged.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous region of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Identify key colors in the top row (excluding 0)
    top_row_colors = [color for color in np.unique(input_grid[0]) if color != 0]

    # Locate the gray region (color 5)
    gray_region_bounds = find_object(input_grid, 5)
    if gray_region_bounds is None:
        return output_grid  # No gray region found, return input as is

    gray_min_row, gray_min_col = gray_region_bounds[0]
    gray_max_row, gray_max_col = gray_region_bounds[1]

    # Determine the vertical extent of replacement
    replace_height = gray_max_row - gray_min_row + 1

     # Replace the gray region based on column position with top_row_colors
    num_colors = len(top_row_colors)
    if num_colors>0:
        color_1 = top_row_colors[0] # red
        
        output_grid[gray_min_row:gray_min_row + replace_height, gray_min_col:gray_min_col+2] = color_1

    if num_colors>1:
        color_2 = top_row_colors[1] # magenta
        output_grid[gray_min_row:gray_min_row + replace_height, gray_min_col+2:gray_min_col+6] = color_2

    if num_colors >2:
        color_3 = top_row_colors[2]
        output_grid[gray_min_row:gray_min_row + replace_height, gray_max_col-2:gray_max_col+1] = color_3

    return output_grid