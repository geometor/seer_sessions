"""
The transformation checks if a column is all blue (1). If the column is all blue, the output column is all green (3).
Otherwise, the output column is all white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same height as the input, and width 1.
    rows = len(input_grid)
    output_grid = np.zeros((rows, 1), dtype=int)

    # Extract the 4th column (index 3) from the input grid.
    check_column = input_grid[:, 3]

    # Check if all elements in the column are blue (1).
    if np.all(check_column == 1):
        output_grid[:, 0] = 3  # Set the output column to green (3)
    else:
        output_grid[:, 0] = 0 # Set to white (0) - default.
    
    # Duplicate this to fill a 3 col array
    output_grid = np.repeat(output_grid,3, axis=1)

    return output_grid