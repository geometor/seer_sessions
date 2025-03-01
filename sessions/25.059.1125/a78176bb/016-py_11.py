"""
The transformation rule is to replicate the initial, top-left to bottom-right, red diagonal line across the grid, effectively creating a repeating diagonal pattern of red pixels and removing the gray pixels.
"""

import numpy as np

def get_initial_diagonal(grid):
    # find the diagonal red pixels starting from top-left
    diagonal_pixels = []
    for i in range(min(grid.shape)):
        if grid[i, i] == 2:
            diagonal_pixels.append((i, i))
        else:
            break # Stop if a non-red pixel is encountered
    return diagonal_pixels

def transform(input_grid):
    """
    Transforms the input grid by replicating the initial red diagonal and removing grey pixels.
    """
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.zeros_like(input_grid)
    initial_diagonal = get_initial_diagonal(input_grid)
    
    if not initial_diagonal:
        return output_grid

    # Determine the length of the initial diagonal.
    diagonal_len = len(initial_diagonal)

    # Replicate the diagonal across the grid.
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # Calculate the diagonal index.
            diag_index = (r - c) % diagonal_len
            
            if 0 <= diag_index < diagonal_len :
                output_grid[r,c] = 2

    return output_grid