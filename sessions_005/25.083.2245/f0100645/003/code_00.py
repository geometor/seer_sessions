"""
Iterate through each row. Find the leftmost color and propagate that color to the
adjacent pixel of a different value, but only if the adjacent pixel is preceded
by a pixel of the leftmost color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by conditionally propagating the leftmost pixel's color across each row.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        seed_color = output_grid[r, 0]  # Get the leftmost pixel's color
        for c in range(1, cols):
            # Conditional Propagation:
            if output_grid[r, c] != seed_color:  # If current pixel is different from leftmost
                if output_grid[r, c-1] == seed_color:  # Check preceding pixel
                    output_grid[r, c] = seed_color  # Set to leftmost color

    return output_grid