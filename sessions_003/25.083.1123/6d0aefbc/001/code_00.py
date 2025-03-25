"""
The transformation rule is to take each element in the input grid and duplicate the values.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_array = np.array(input_grid)
    height, width = input_array.shape
    output_height = height * 2
    output_width = width * 2
    output_array = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for i in range(height):
        for j in range(width):
            output_array[i*2, j*2] = input_array[i, j]
            output_array[i*2+1, j*2] = input_array[i, j]
            output_array[i*2, j*2+1] = input_array[i, j]
            output_array[i*2+1, j*2+1] = input_array[i, j]

    return output_array.tolist()