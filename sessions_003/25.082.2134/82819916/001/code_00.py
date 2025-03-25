"""
The transformation identifies colored object in a row, then copies and inserts it, where that cell has '0' (white/background color) to the right.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid.
    for i in range(rows):
        # Check if the current row contains any non-zero values.
        if np.any(input_grid[i] != 0):
            # If there are colored objects, iterate the colors and
            # replicate the object based on the following rule, by
            # inserting a duplicate object immediately to the right
            # of the object.
          
            j = 0
            while j < cols:

                if (j < cols - 1) and input_grid[i,j] != 0:

                    if input_grid[i, j] != input_grid[i,j+1]:
                        if input_grid[i, j+1] == 0:
                            #   If that is not true and the value next to it is 0, then
                            # copy the current element and insert the copy immediately to
                            # the right of the current object.

                            # shift elements to the right to insert
                            output_grid[i, j+2:] = output_grid[i, j+1:-1]
                            output_grid[i,j+1] = input_grid[i,j]
                            j += 1 # skip newly inserted
                j+= 1
                

    # Return the modified grid.
    return output_grid