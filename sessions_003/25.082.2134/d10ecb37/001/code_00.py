"""
Extract the first two columns from the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Extract the first two columns.
    output_array = input_array[:, :2]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid