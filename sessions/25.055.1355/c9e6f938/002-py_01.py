"""
The input grid is transformed into the output grid by duplicating any column that contains at least one orange (7) pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating columns containing the color 7.
    """
    input_grid = np.array(input_grid)
    num_rows, num_cols = input_grid.shape
    output_grid_cols = []

    # Iterate through the input grid columns
    for j in range(num_cols):
        column = input_grid[:, j]
        # Check if the column contains at least one orange (7) pixel
        if 7 in column:
            # Duplicate the column
            output_grid_cols.append(column)
            output_grid_cols.append(column)
        else:
            # Output the original column
            output_grid_cols.append(column)
    
    # Convert the list of columns to a NumPy array (grid)
    output_grid = np.column_stack(output_grid_cols)
    return output_grid.tolist()