"""
Extract the center column(s) from the input grid.  If the input grid has an odd number of columns,
copy the center column to the output grid. If the input grid has an even number of columns,
copy the two center-most columns.  Set all other values in the output grid to 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the center column(s) and setting all other values to 0.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    center_col_index = cols // 2

    if cols % 2 != 0:  # Odd number of columns
        # Extract the center column.
        selected_column = input_grid[:, center_col_index]

        # Set the center column of the output grid.
        output_grid[:, center_col_index] = selected_column
    else:  # Even number of columns
        # Extract and copy center-left column
        selected_left_column = input_grid[:, center_col_index - 1]
        output_grid[:, center_col_index -1] = selected_left_column

        # Extract and copy center-right column.
        selected_right_column = input_grid[:, center_col_index]
        output_grid[:, center_col_index] = selected_right_column

    return output_grid