```python
"""
The transformation takes the left side of the input grid, reverses the order of the columns, and places those after column of 5s. Then copies the bottom row of the left side of input grid, and copies it to the rightmost section of the output, reading upwards.
"""

import numpy as np

def get_left_side(grid):
    #find the separator column
    separator_col = np.where(grid[0,:] == 5)[0][0]
    #return the grid up to the seperator
    return grid[:, :separator_col]

def reverse_columns(grid):
    return np.fliplr(grid)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Get the left side of the input grid
    left_side = get_left_side(input_grid)

    # Reverse the columns of the left side
    reversed_left_side = reverse_columns(left_side)

    # Find the separator column index
    separator_col_index = input_grid.shape[1] // 2 -1
    
    # 1. Copy left_side to output
    output_grid[:, :left_side.shape[1]] = left_side
    
    # 2. Copy Separator Column
    output_grid[:, separator_col_index] = input_grid[:, separator_col_index]

    # 3. Copy the reversed left side to the output
    output_grid[:, separator_col_index + 1:separator_col_index + 1 + reversed_left_side.shape[1]] = reversed_left_side
    
    # 4. copy the bottom row up of the left side of input, to right side of output
    bottom_up_left = left_side[::-1, :].flatten()
    output_grid[: , -bottom_up_left.shape[0]:] =  bottom_up_left.reshape(output_grid.shape[0],-1)

    return output_grid
```