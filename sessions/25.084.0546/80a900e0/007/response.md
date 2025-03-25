```python
"""
Copies colors from "source pixels" (white cells with non-blue/non-white colors) to other white cells
within the grid, following the checkerboard pattern defined by alternating white (0) and blue (1) cells.
Propagation extends diagonally in all four directions, maintaining row/column parity, stopping at blue cells.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to determine checkerboard parity (2x2)
    def get_parity(r, c):
        return (r % 2, c % 2)

    # Helper function to check if a cell is white in the checkerboard
    def is_white_checkerboard(r, c):
        return get_parity(r, c) == (0, 0) or get_parity(r, c) == (1, 1)

    # Iterate through the input grid to find source pixels
    for r in range(rows):
        for c in range(cols):
            # Identify Source Pixels: White (0) cells with a non-blue/non-white color on white checkerboard
            if input_grid[r, c] != 1 and input_grid[r, c] != 0 and is_white_checkerboard(r, c):
                source_color = input_grid[r, c]

                # Propagate color to target pixels based on checkerboard parity and diagonal
                for r2 in range(rows):
                    for c2 in range(cols):
                        # Target must be on white checkerboard, be currently white, and be diagonal
                        if is_white_checkerboard(r2, c2) and output_grid[r2, c2] == 0:
                            if abs(r - r2) == abs(c - c2) and (r - r2) % 2 == 0:
                                output_grid[r2, c2] = source_color
    return output_grid
```