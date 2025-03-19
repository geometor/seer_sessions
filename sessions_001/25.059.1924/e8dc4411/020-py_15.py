"""
The transformation involves identifying the right-most azure pixel and replicating it to the right if a yellow pixel is diagonally down and to its right. Yellow pixels and the background remain unchanged.
"""

import numpy as np

def find_rightmost_azure(grid):
    """Finds the row and column index of the right-most azure pixel."""
    rows, cols = grid.shape
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8:
                azure_pixels.append((r, c))
    if not azure_pixels:
        return None
    return max(azure_pixels, key=lambda x: x[1])


def transform(input_grid):
    """
    Transforms the input grid based on the described rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the right-most azure pixel
    rightmost_azure = find_rightmost_azure(input_grid)

    if rightmost_azure:
        r, c = rightmost_azure
        # Check for yellow pixel diagonally down and to the right
        if r + 1 < rows and c + 1 < cols and input_grid[r + 1, c + 1] == 4:
            # Replicate azure pixel to the right
            if c + 1 < cols:
              output_grid[r, c + 1] = 8

    return output_grid