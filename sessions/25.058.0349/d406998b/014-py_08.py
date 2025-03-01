"""
Iterate through the input grid. 
If a cell is on the top row and has a value of 0 and is directly to the left of one or more values of 5, change the value to a 3. 
If a cell is a value of 0, is not on the top row, and is directly above or below a 3, change the value to 3.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels, phase 1, 0 -> 3
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 0:
                if r == 0: # top row
                    if c + 1 < cols and output_grid[r,c+1] == 5:
                        output_grid[r,c] = 3
                else: # not top row
                    if output_grid[r-1,c] == 3 or (r+1 < rows and output_grid[r+1, c] == 3):
                        output_grid[r,c] = 3
    
    return output_grid