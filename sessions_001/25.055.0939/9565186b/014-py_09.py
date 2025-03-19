"""
Replace azure pixels in the middle row with gray pixels; leave all other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows in the grid
    rows = output_grid.shape[0]
    
    # Iterate through the grid
    for r in range(rows):
        for c in range(output_grid.shape[1]):
            # Find azure pixels (color 8)
            if output_grid[r,c] == 8:
                #that are located in the middle row
                if r == rows // 2:
                    #change them to gray (color 5)
                    output_grid[r,c] = 5
    
    # Return the modified grid
    return output_grid