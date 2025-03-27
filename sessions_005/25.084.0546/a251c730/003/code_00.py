"""
1.  **Identify Background:** Determine the background colors as the colors in the top-left and bottom-right corners of the input grid.
2.  **Crop:** Find the bounding box that encompasses all pixels *not* of the background colors. This defines a rectangular region containing the core pattern.
3.  **Extract:** Extract the subgrid defined by the bounding box. This subgrid is the output.
"""

import numpy as np

def get_bounding_box(grid, background_colors):
    rows, cols = np.where(~np.isin(grid, background_colors))
    if rows.size > 0:
        min_row, max_row = rows.min(), rows.max()
        min_col, max_col = cols.min(), cols.max()
        return min_row, max_row, min_col, max_col
    else:
        return 0, 0, 0, 0 # Handle empty case

def transform(input_grid):
    # Convert input to a NumPy array
    grid = np.array(input_grid)

    # Identify background colors
    background_colors = [grid[0, 0], grid[-1, -1]]

    # Crop to the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(grid, background_colors)
    cropped_grid = grid[min_row:max_row+1, min_col:max_col+1]
    
    return cropped_grid.tolist()