"""
Sorts the pixel values within each row of the input grid in ascending order.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by sorting each row in ascending order.
    """
    # Convert input to a NumPy array
    input_array = np.array(input_grid)
    
    # Initialize the output array
    output_array = np.empty_like(input_array)

    # Iterate through each row and sort it.
    for i in range(input_array.shape[0]):
        output_array[i, :] = np.sort(input_array[i, :])

    return output_array.tolist()