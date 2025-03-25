"""
The rule extracts a 3x3 subgrid from the input grid. The subgrid is the smallest 3x3 area that contains all the non-white pixels of the input grid. If no such subgrid exists, return a 3x3 grid of all zeros.
"""

import numpy as np

def find_smallest_bounding_subgrid(input_grid):
    # Find indices of all non-white pixels
    non_white_indices = np.argwhere(input_grid != 0)

    # If there are no non-white pixels, return None
    if len(non_white_indices) == 0:
        return None

    # Find the min and max row and col to define the bounding box
    min_row, max_row = np.min(non_white_indices[:, 0]), np.max(non_white_indices[:, 0])
    min_col, max_col = np.min(non_white_indices[:, 1]), np.max(non_white_indices[:, 1])

    # Calculate bounding box dimensions
    bounding_box_height = max_row - min_row + 1
    bounding_box_width = max_col - min_col + 1

    # If the bounding box is larger than 3x3, no 3x3 subgrid can contain all non-white pixels.
    if bounding_box_height > 3 or bounding_box_width > 3:
        return None

    # Iterate through all possible 3x3 subgrids and check if they contain the bounding box
    for row_start in range(input_grid.shape[0] - 2):
        for col_start in range(input_grid.shape[1] - 2):
            # Check if this 3x3 subgrid contains all non-white pixels
             contains_all = True
             for r,c in non_white_indices:
                if not (row_start <= r < row_start + 3 and col_start <= c < col_start + 3):
                    contains_all = False
                    break
             if contains_all:
                return input_grid[row_start:row_start+3, col_start:col_start+3]

    return None

def transform(input_grid):
    """
    Transforms a 9x9 input grid into a 3x3 output grid.  It finds the smallest
    3x3 subgrid that contains all non-white pixels.
    """
    # Find the smallest bounding subgrid
    output_grid = find_smallest_bounding_subgrid(np.array(input_grid))
    
    if output_grid is None:
        # handle edge case, return a grid with 0's
        output_grid = np.zeros((3,3),dtype=int)

    return output_grid.tolist()