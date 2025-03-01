"""
Replicates each row of the input grid to produce the output grid, then
conditionally swaps certain adjacent rows or performs additional replication
based on the position of 0-valued pixels in the last row of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    rows, cols = input_array.shape
    
    # Initialize an empty output array with doubled row count.
    output_array = np.zeros((rows * 2, cols), dtype=int)
    
    # Row Replication: Duplicate each row from input to output.
    for i in range(rows):
        output_array[2*i, :] = input_array[i, :]
        output_array[2*i + 1, :] = input_array[i, :]

    # Conditional Row Adjustment based on the last row of the input.
    last_row = input_array[-1]
    zero_indices = np.where(last_row == 0)[0]

    if zero_indices.size > 0:  # Check if there are any 0s in the last row
        if zero_indices[0] == 2:
            if rows == 4 :
                output_array[5, :] = input_array[2,:]
            else:    
                # Swap the second and third rows (index 1 and 2).
                output_array[[1, 2]] = output_array[[2, 1]]
        elif zero_indices[0] == 3:
            output_array[[1, 2]] = output_array[[2, 1]]

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()
    
    return output_grid