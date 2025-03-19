"""
The transformation extracts a subgrid from the input grid. The subgrid is defined by the bounding box of the green pixels (value 3). All green pixels within this subgrid are then changed to gray (value 5) in the output grid.
"""

import numpy as np

def get_green_bounding_box(grid):
    """
    Finds the bounding box of green pixels in the grid.
    Returns (min_row, max_row, min_col, max_col) or None if no green pixels are found.
    """
    green_coords = np.argwhere(grid == 3)
    if green_coords.size == 0:
        return None
    
    min_row = np.min(green_coords[:, 0])
    max_row = np.max(green_coords[:, 0])
    min_col = np.min(green_coords[:, 1])
    max_col = np.max(green_coords[:, 1])
    
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    
    # Get the bounding box of green pixels
    bbox = get_green_bounding_box(input_grid)
    if bbox is None:
        return input_grid.tolist()  # Return original if no green pixels

    min_row, max_row, min_col, max_col = bbox
    
    # Extract the subgrid based on the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()

    # Change green (3) to gray (5) in the output grid
    output_grid[output_grid == 3] = 5

    return output_grid.tolist()