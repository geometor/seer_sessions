"""
The input grid is transformed into the output grid by duplicating each column. This effectively doubles the width of the grid while maintaining the original height.
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

    # Initialize an empty list to store the output.
    output_grid = []

    # Iterate through each row of the input array.
    for row in input_array:
        # Initialize a new row for the output.
        new_row = []
        # Iterate through each column (pixel) in the current row.
        for pixel in row:
            # Duplicate each pixel and add it to the new row.
            new_row.extend([pixel, pixel])  # Add the pixel twice
        # Add the expanded row to the output grid.
        output_grid.append(new_row)

    return output_grid