"""
The transformation rule involves transposing the input grid and then reversing each row of the transposed grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Transpose the array
    transposed_array = input_array.T

    # Reverse each row of the transposed array
    output_array = np.flip(transposed_array, axis=1)
    
    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid