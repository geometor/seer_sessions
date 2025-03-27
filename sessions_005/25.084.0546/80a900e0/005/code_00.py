"""
Copies colors from "source pixels" (white cells with non-blue/non-white colors) to other cells
within the grid, following the checkerboard pattern defined by alternating white (0) and blue (1) cells.
Propagation extends diagonally in all four directions, maintaining row/column parity.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to determine checkerboard parity
    def get_parity(r, c):
        return (r % 2, c % 2)

    # Iterate through the input grid to find source pixels
    for r in range(rows):
        for c in range(cols):
            # Identify Source Pixels: White (0) cells with a non-blue/non-white color
            if input_grid[r, c] != 1 and input_grid[r, c] != 0:
                if get_parity(r,c) == (0,1) or get_parity(r,c) == (1,0):
                    continue # skip if not on a '0'
                
                source_color = input_grid[r, c]
                source_parity = get_parity(r, c)

                # Propagate color to target pixels based on checkerboard parity
                for r2 in range(rows):
                    for c2 in range(cols):
                        target_parity = get_parity(r2, c2)
                        if target_parity == source_parity:
                            # check for diagonal
                            if abs(r-r2) == abs(c-c2) and (r-r2) % 2 == 0:
                                output_grid[r2, c2] = source_color
    return output_grid