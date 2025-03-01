"""
Transforms an input grid to a 3-column wide output grid. The output grid's center column
contains an 8 for each row where the corresponding input column (identified as containing a '1') had a '1', and 0 otherwise.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid: same height as input, width 3, filled with 0s.
    output_height = input_grid.shape[0]
    output_grid = np.zeros((output_height, 3), dtype=int)

    # Identify columns in the input grid containing the value '1' (blue).
    columns_with_blue = np.where(np.any(input_grid == 1, axis=0))[0]

    # Iterate through identified columns.
    for col_index in columns_with_blue:
        # Extract the current column from the input grid.
        column = input_grid[:, col_index]

        # Map values: 1 becomes 8, others become 0.
        mapped_column = np.where(column == 1, 8, 0)

        # Place the mapped column into the center column (index 1) of the output grid.
        output_grid[:, 1] = mapped_column

    return output_grid