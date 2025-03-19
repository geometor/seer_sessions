"""
Replaces green (3) pixels with azure (8) pixels if they are part of a horizontal contiguous sequence of green pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing certain green pixels with azure pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is green (3)
            if input_grid[r, c] == 3:
                # Check for horizontal contiguity
                is_contiguous = False
                if c > 0 and input_grid[r, c - 1] == 3:
                    is_contiguous = True
                if c < cols - 1 and input_grid[r, c + 1] == 3:
                    is_contiguous = True

                # Replace with azure (8) if contiguous
                if is_contiguous:
                    output_grid[r, c] = 8

    return output_grid