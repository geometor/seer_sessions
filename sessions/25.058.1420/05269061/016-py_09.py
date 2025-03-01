"""
Extends the existing colored diagonals in the input grid, wrapping around the edges, and using the color sequence azure, green, yellow, repeating.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending the diagonal color patterns.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    color_sequence = [8, 3, 4]  # Azure, Green, Yellow

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:  # If the cell is white
                # Determine the diagonal index and corresponding color
                diagonal_index = (c - r) % len(color_sequence)
                # Adjust for negative modulo, not needed for python
                output_grid[r, c] = color_sequence[diagonal_index]

    return output_grid