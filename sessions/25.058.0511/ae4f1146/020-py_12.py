"""
Extracts a 3x3 subgrid from the input grid, focusing on a central region 
containing only blue (1) and azure (8) pixels.
"""

import numpy as np

def extract_subgrid(grid, row_start, row_end, col_start, col_end):
    """Extracts a subgrid from the given grid."""
    return grid[row_start:row_end, col_start:col_end]

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # find all blue and azure cells
    blue_azure_indices = np.where((input_grid == 1) | (input_grid == 8))
    blue_azure_coords = list(zip(blue_azure_indices[0], blue_azure_indices[1]))
    
    # compute the minimum bounding box
    min_row = np.min(blue_azure_indices[0])
    max_row = np.max(blue_azure_indices[0])
    min_col = np.min(blue_azure_indices[1])
    max_col = np.max(blue_azure_indices[1])    

    output_grid = np.zeros((max_row-min_row+1, max_col-min_col+1),dtype=int)    
    for r,c in blue_azure_coords:
        output_grid[r-min_row,c-min_col]=input_grid[r,c]

    return output_grid