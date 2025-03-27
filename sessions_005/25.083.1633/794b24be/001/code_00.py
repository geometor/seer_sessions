"""
Transforms a 3x3 input grid (containing 0s and 1s) to a 3x3 output grid (containing 0s and 2s) 
based on these rules:
1. If the top-left cell is '1', replace *all* '1's in the entire grid with '2's.
2. If the first entry in a row has a '1', change that element to `2`.
3. If the first and second entry in a row has a `1`, change those two elements to `2`.

"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    output_grid = np.copy(input_grid)  # Initialize output as a copy

    # Check if the top-left cell is 1
    if input_grid[0, 0] == 1:
        # Replace all 1s with 2s
        output_grid[output_grid == 1] = 2
        return output_grid
    
    # iterate through rows
    for i in range(3):
        first_one = -1

        # check each cell
        for j in range(3):
            if input_grid[i,j] == 1:
                first_one = j
                break

        if first_one != -1:
           if first_one == 0:
               output_grid[i,first_one] = 2

               # change next
               if first_one+1 < 3 and input_grid[i,first_one+1] == 1:
                   output_grid[i, first_one+1] = 2
                   

    return output_grid