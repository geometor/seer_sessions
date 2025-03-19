"""
Extracts the top-right 3x3 subgrid from the input grid and returns it as the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    rows, cols = input_array.shape
    
    # Extract the top-right 3x3 subgrid.
    output_array = input_array[0:3, -3:]
    
    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid