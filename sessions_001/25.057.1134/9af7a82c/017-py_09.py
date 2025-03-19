"""
The transformation rule extracts all non-zero values from each column of the input grid, and concatenates them into a single row to form the output grid. Columns containing only zeros are ignored.
"""

import numpy as np

def transform(input_grid):
    # Initialize an empty list to store the non-zero values
    output_list = []

    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)
    
    # Iterate through each column of the input grid
    for j in range(input_grid.shape[1]):
        # Extract the current column
        column = input_grid[:, j]
        
        # Filter out the non-zero values from the column
        non_zero_values = column[column != 0]
        
        # Extend the output list with the non-zero values
        output_list.extend(non_zero_values)

    # Convert the output list to output numpy array. If the output_list is empty, it should return an empty 1x0 array, not 0x0.
    if len(output_list) >0:
        output_grid = np.array(output_list).reshape(1,-1)
    else:
        output_grid = np.empty((1,0),dtype=int)
    return output_grid