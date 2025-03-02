"""
The transformation removes all instances of the color red (2) from the input grid and extracts a 4x4 subgrid.
The subgrid appears to be constructed by selecting specific columns from the input.
"""

import numpy as np

def get_column(grid, col_index):
    return [row[col_index] for row in grid]

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    
    # 1. Identify Target Colors: Filter out red (2)
    filtered_grid = input_grid[input_grid != 2]
    
    # rebuild the input grid with the same dimensions, remove the filtered color
    rows, cols = input_grid.shape
    filtered_grid = filtered_grid.reshape(-1, cols)

    # Extract the specific set of columns that create a 4x4 grid
    output_grid = np.array([
        get_column(filtered_grid, 5),  # maroon
        get_column(filtered_grid, 1),  # yellow
        get_column(filtered_grid, 0),  # white
        get_column(filtered_grid, 1),  # yellow
    ]).T  # transpose, to align as columns, not rows

    # return the result
    return output_grid.tolist()