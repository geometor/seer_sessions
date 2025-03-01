"""
The input grid is transformed into the output grid by duplicating each column. The height of the grid remains the same. The width of the output grid is double the width of the input grid. Each column in the input grid becomes two identical adjacent columns in the output grid. The color of each pixel within a column is preserved.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list to a NumPy array.
    input_array = np.array(input_grid)

    # Get the dimensions of the input array.
    rows, cols = input_array.shape

    # Create a new array with doubled width.
    output_array = np.empty((rows, cols * 2), dtype=input_array.dtype)

    # Iterate through the columns of the input array.
    for i in range(cols):
        # Duplicate each column into the output array.
        output_array[:, 2*i] = input_array[:, i]
        output_array[:, 2*i + 1] = input_array[:, i]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid