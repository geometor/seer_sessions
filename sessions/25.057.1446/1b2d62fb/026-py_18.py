"""
Extracts a subgrid centered on the central, solid-color column of the input grid. 
The subgrid's height matches the input's height. 
The central column's values are then mapped: 1 becomes 8, and all other values become 0. 
These mapped values are placed in a centered column of the output grid, 
with the mapped '1' (now 8) at the center row. The rest of the output is filled with 0s.
"""

import numpy as np

def find_central_solid_column(grid):
    """Finds the index of the central, solid-color column in a grid."""
    height, width = grid.shape
    center_x = width // 2
    central_column = grid[:, center_x]
    if np.all(central_column == central_column[0]):
        return center_x
        
    # handle cases where the central column is not solid
    for i in range(max(center_x,width-center_x)):
        if center_x-i >=0:
            column = grid[:, center_x-i]
            if np.all(column == column[0]):
                return center_x-i
        if center_x+i < width:
            column = grid[:, center_x+i]
            if np.all(column == column[0]):
                return center_x+i    
    
    return -1  # No solid central column found


def transform(input_grid):
    # Find the central solid-color column
    center_column_index = find_central_solid_column(input_grid)

    # Extract the relevant column
    column = input_grid[:, center_column_index]  # no subgrid extraction, it's about the height.
    
    # Determine output grid dimensions
    output_height = input_grid.shape[0]
    unique_values = len(np.unique(column))
    output_width = 3

    # Initialize output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map values and construct the central output column
    mapped_column = np.where(column == 1, 8, 0)

    
    # Place the mapped column in the output
    output_grid[:, 1] = mapped_column
    # for i, value in enumerate(mapped_column):
    #     output_grid[i, output_width // 2] = value

    return output_grid