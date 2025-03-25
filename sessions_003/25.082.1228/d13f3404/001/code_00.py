"""
Diagonally expand the non-zero elements of the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    in_rows, in_cols = input_grid.shape
    
    # Determine output grid dimensions
    out_rows = in_rows + in_cols - 1
    out_cols = in_rows + in_cols - 1
    
    # Initialize output grid with zeros
    output_grid = np.zeros((out_rows, out_cols), dtype=int)

    # Iterate through input grid and propagate non-zero values diagonally
    for r in range(in_rows):
        for c in range(in_cols):
            if input_grid[r, c] != 0:
                # Propagate the value diagonally
                for i in range(min(out_rows - r, out_cols - c)):
                    output_grid[r + i, c + i] = input_grid[r, c]

    return output_grid