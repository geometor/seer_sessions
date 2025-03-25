"""
The task involves transforming an input grid of colored pixels into a smaller output grid.
The transformation extracts and rearranges colored objects from the input.  The core
operation is to extract a subgrid that contains all the non-zero pixels, then crop any
remaining all-zero rows/columns from the top, left, right, and bottom.
"""

import numpy as np

def get_bounding_box(grid):
    # Find rows and cols with non-zero elements
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    # Get the indices of the first and last True values
    min_row, max_row = np.where(rows)[0][[0, -1]] if np.any(rows) else (0,0)
    min_col, max_col = np.where(cols)[0][[0, -1]] if np.any(cols) else (0,0)
    return min_row, max_row, min_col, max_col

def crop_empty_edge(grid):
    # get the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(grid)

    # crop the grid
    cropped_grid = grid[min_row:max_row+1, min_col:max_col+1]
    
    return cropped_grid
    

def transform(input_grid):
    """
    Transforms the input grid by extracting a subgrid containing all non-zero pixels,
    and then cropping any remaining all-zero rows/columns.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Crop the grid based on bounding box
    output_grid = crop_empty_edge(input_grid)

    return output_grid.tolist()