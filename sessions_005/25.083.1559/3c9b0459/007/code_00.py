"""
The transformation rule performs a column-to-row transposition with a specific element mapping. Each column of the input grid becomes a row in the output grid. Specifically, the element at index `[i, j]` in the input grid (where `i` is the row index and `j` is the column index) is moved to index `[j, (number_of_columns - 1) - i]` in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Get the number of rows and columns
    num_rows, num_cols = input_array.shape

    # Initialize an empty output array with the same dimensions
    output_array = np.empty_like(input_array)

    # Iterate over the input array's indices
    for i in range(num_rows):
        for j in range(num_cols):
            # Apply the transformation rule: input[i, j] -> output[j, (num_cols - 1) - i]
            output_array[j, (num_cols - 1) - i] = input_array[i, j]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid