"""
The transformation rotates the input grid by 180 degrees. The output grid is the result of rotating the entire input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees using numpy's rot90 function twice.
    output_array = np.rot90(input_array, 2)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid