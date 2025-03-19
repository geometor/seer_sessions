"""
Rotate the input grid 90 degrees clockwise.
Invert Colors on the main diagonal: The colors on the main diagonal are flipped. The top left, the center and the bottom right corner change places, the content of the bottom left corner becomes the top left corner.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.rot90(input_grid, k=-1) # Rotate 90 degrees clockwise

    # Get dimensions
    rows, cols = output_grid.shape
    
    # Create a copy for modifications, to handle inplace change
    modified_grid = np.copy(output_grid)

    # Reflect/mirror the relevant corner cells.
    modified_grid[0,0] = output_grid[2,0]
    modified_grid[0,1] = output_grid[1,0]
    modified_grid[0,2] = output_grid[0,0]
    modified_grid[1,2] = output_grid[0,1]
    modified_grid[2,2] = output_grid[0,2]
    modified_grid[2,1] = output_grid[1,2]
    modified_grid[1,0] = output_grid[2,1]
    modified_grid[2,0] = output_grid[2,2]

    return modified_grid