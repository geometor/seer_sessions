"""
Replicates each row of the input grid to produce the output grid, then swaps
certain adjacent rows.
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

    # Swap the second and third rows.
    output_array[[1, 2]] = output_array[[2, 1]]

        # Swap the forth and fifth rows.
    output_array[[3, 4]] = output_array[[4, 3]]    

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()
    
    return output_grid