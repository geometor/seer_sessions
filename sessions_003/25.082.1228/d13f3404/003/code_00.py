"""
Diagonally expand the non-zero elements of the input grid to create the output grid. The output grid's dimensions are (rows + cols) x (rows + cols), where rows and cols are the dimensions of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    in_rows, in_cols = input_grid.shape
    
    # Determine output grid dimensions
    out_size = in_rows + in_cols
    
    # Initialize output grid with zeros
    output_grid = np.zeros((out_size, out_size), dtype=int)

    # Iterate through input grid and propagate non-zero values diagonally
    for r in range(in_rows):
        for c in range(in_cols):
            if input_grid[r, c] != 0:
                # Propagate the value diagonally
                for i in range(out_size):
                    if r + i < out_size and c + i < out_size:
                        output_grid[r + i, c + i] = input_grid[r, c]

    return output_grid