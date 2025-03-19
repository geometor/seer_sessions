"""
The input grid is transformed into the output grid by duplicating each column of the input. The width of the grid is doubled, and the height remains the same. The colors in each column are preserved during the duplication process. Each original column in the input grid becomes two identical, adjacent columns in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each column.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with duplicated columns.
    """
    # Convert the input list to a NumPy array for easier manipulation.
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