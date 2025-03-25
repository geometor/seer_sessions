"""
The input grid is vertically mirrored and then stacked below the original grid, effectively doubling the number of rows while preserving the column count.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Create a reflected version of the input grid by flipping it vertically.
    reflected_np = np.flipud(input_np)

    # combine the original grid with the reflected grid.
    output_np = np.concatenate((input_np, reflected_np), axis=0)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_np.tolist()
    
    return output_grid