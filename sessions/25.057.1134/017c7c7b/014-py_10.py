"""
The transformation takes a grid with a blue line, changes the blue line to red, and adds three rows at the bottom of the grid which continues the pattern - white, white, red, red.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid by copying the input grid and changing the datatype to allow modification.
    output_grid = input_grid.astype(int)
    
    # Find the blue pixels (value 1) and change them to red (value 2) in the output grid.
    output_grid[output_grid == 1] = 2

    # Get dimensions of the original input grid.
    rows, cols = input_grid.shape
    
    # Create a new array of zeros with extra rows
    added_rows = np.zeros((3, cols), dtype=int)

    #Set pattern of the added rows.
    added_rows[0, :] = 0 # white
    added_rows[1, 1] = 2 #red
    added_rows[2, 1] = 2 #red

    # Concatenate the original grid with added rows using vstack
    output_grid = np.vstack((output_grid, added_rows))    

    return output_grid