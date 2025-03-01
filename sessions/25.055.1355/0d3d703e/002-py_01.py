"""
Increment each integer in the input grid by 1 to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Create a new array by adding 1 to each element of the input array.
    output_array = input_array + 1
    
    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid