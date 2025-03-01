"""
The transformation rule is to swap the first and second columns of the input grid to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Swaps the first and second columns of the input grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Create a copy of the input array to serve as the output grid.
    output_array = np.copy(input_array)

    # Swap the first and second columns.
    output_array[:, [0, 1]] = output_array[:, [1, 0]]
    
    # Convert back to python list
    output_grid = output_array.tolist()

    return output_grid