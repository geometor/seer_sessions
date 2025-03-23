"""
The transformation rule is to transpose the input grid and then reverse the order of the rows. 
In other words, create the output grid by reading the input grid in reverse column-major order.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Transpose the array (swap rows and columns)
    transposed_array = input_array.T

    # Reverse the order of the rows
    output_array = np.flipud(transposed_array)
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid