"""
The transformation rule is a column-to-row transposition with a cyclic upward shift of elements within each column.
Each column of the input grid becomes a row in the output grid. Before becoming a row, each column's elements
are rotated upwards by one position: the top element moves to the bottom, and all other elements shift up.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Get the number of rows and columns in the input.
    num_rows, num_cols = input_array.shape

    # Initialize an empty output array. Using zeros is fine since we are going to replace with new values
    output_array = np.zeros_like(input_array)

    # Iterate through each column.
    for j in range(num_cols):
        # Extract the current column.
        column = input_array[:, j]

        # Perform the cyclic upward shift.
        rotated_column = np.roll(column, -1)

        # Assign the rotated column to the corresponding row in the output array.
        output_array[j, :] = rotated_column

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid