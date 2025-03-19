"""
Identifies a green (color 3) region in the input grid, then creates an output
grid where: the top row is a copy of the top row of the green region, the width
is the same as the width of the green region, and the height is the width of
the green region - 1, and the rest of the cells are filled with black (0).
"""

import numpy as np

def find_green_object(grid):
    """
    Finds the bounding box of the green (color 3) region.
    Returns (min_row, max_row, min_col, max_col) or None if no green is found.
    """
    rows, cols = np.where(grid == 3)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    grid = np.array(input_grid)
    
    # 1. Identify the Green Object:
    green_bounds = find_green_object(grid)
    if green_bounds is None:
        return [[]]  # Return empty grid if no green object

    min_row, max_row, min_col, max_col = green_bounds

    # 2. Determine Output Dimensions:
    width = max_col - min_col + 1
    height = width -1
    
    #initialize output
    output_grid = np.zeros((height, width), dtype=int)

    # 3. Copy Top Row of Green Object:
    top_row_green = grid[min_row, min_col:max_col+1]
    output_grid[0, :] = top_row_green

    
    # 4. return output
    return output_grid.tolist()