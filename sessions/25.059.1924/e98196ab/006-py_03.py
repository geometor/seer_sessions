"""
The transformation rule focuses on the relationship between azure ('8') and blue ('1') pixels.
An azure pixel ('8') in the input grid is retained in the output grid *only if* it has at least one adjacent blue ('1') pixel (horizontally, vertically, or diagonally).
All other pixels in the output grid are set to white ('0').
"""

import numpy as np

def check_adjacency(grid, r, c, target_color):
    """Checks if a cell at (r, c) has any adjacent cells of the target_color."""
    rows, cols = grid.shape
    for i in range(max(0, r-1), min(rows, r+2)):
        for j in range(max(0, c-1), min(cols, c+2)):
            if (i != r or j != c) and grid[i, j] == target_color:
                return True
    return False

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is azure ('8')
            if input_grid[r, c] == 8:
                # Check for adjacent blue ('1') pixels
                if check_adjacency(input_grid, r, c, 1):
                    # If adjacent to blue, copy '8' to the output grid
                    output_grid[r, c] = 8

    return output_grid