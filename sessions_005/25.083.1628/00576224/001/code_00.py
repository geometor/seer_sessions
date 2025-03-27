"""
Replicates a 2x2 input grid to create a 6x6 output grid. The replication involves 
alternating rows and swapping columns in every other row based on the original 2x2 input.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 6x6 numpy array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Get the input grid dimensions (which are assumed to be 2x2).
    rows, cols = input_grid.shape

    # Populate the output grid.
    for i in range(6):
        for j in range(6):
            # Determine the source row and column in the input grid.
            input_row = i % rows
            input_col = j % cols

            # Perform the row alternation and column swapping.
            if (i // rows) % 2 == 1:  # Check for every other 2x2 block of rows.
                output_grid[i, j] = input_grid[input_row, 1 - input_col]
            else:
                output_grid[i, j] = input_grid[input_row, input_col]

    return output_grid