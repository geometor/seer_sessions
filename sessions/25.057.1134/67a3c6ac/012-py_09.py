"""
The transformation rule is a matrix transposition. The input grid is reflected across its main diagonal.  This means that each element at row *r* and column *c* in the input grid is moved to row *c* and column *r* in the output grid. The values (colors) of the elements remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the NumPy array.
    output_array = input_array.transpose()

    # Convert the output NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid