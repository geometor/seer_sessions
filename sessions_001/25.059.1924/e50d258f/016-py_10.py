"""
1. Identify the Sub-grid: Locate the smallest rectangular sub-grid within the input grid that contains all non-white pixels, starting from the upper-left corner.
2. Crop: Extract this sub-grid.
3. Filter: Exclude all white pixels.
"""

import numpy as np

def find_non_white_subgrid(grid):
    # Find rows and cols with non-white pixels
    rows, cols = np.where(grid != 0)
    
    if len(rows) == 0:  # Handle empty case
        return (0, 0, 0, 0)

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return (min_row, max_row + 1, min_col, max_col + 1)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the boundaries of the subgrid
    min_row, max_row, min_col, max_col = find_non_white_subgrid(input_grid)
    
    # Crop the subgrid
    cropped_grid = input_grid[min_row:max_row, min_col:max_col]
    
    return cropped_grid.tolist()