"""
1. Identify Columns for Duplication: Find all columns that either contain an orange (7) pixel or contain any other non-black (0) pixel.
2. Duplicate Columns: Duplicate all identified columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating columns containing the color 7 or any non-black pixel.
    """
    input_grid = np.array(input_grid)
    num_rows, num_cols = input_grid.shape
    output_grid_cols = []

    # Iterate through the input grid columns
    for j in range(num_cols):
        column = input_grid[:, j]
        # Check if the column contains at least one orange (7) pixel or any non-black pixel.
        if 7 in column or any(pixel != 0 for pixel in column):
            # Duplicate the column
            output_grid_cols.append(column)
            output_grid_cols.append(column)
        else:
            # Output the original column.
            output_grid_cols.append(column) # Keep the black columns, although is not necessary, as they are not duplicated.
    
    # Convert the list of columns to a NumPy array (grid)
    output_grid = np.column_stack(output_grid_cols)
    return output_grid.tolist()