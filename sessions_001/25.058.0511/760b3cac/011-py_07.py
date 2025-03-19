"""
1.  **Identify Azure Pixels:** Locate all pixels in the input grid that have the color azure (value 8).
2.  **Horizontal Fill:** For each azure pixel found, extend it horizontally to the right, changing all pixels to azure (8) until the right edge of the grid is reached. Each azure pixel is effectively the starting point of a horizontal line that spans to the grid's right border.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending azure (8) pixels to the right.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is azure
            if output_grid[r, c] == 8:
                # Extend the azure color to the right
                for c2 in range(c + 1, cols):
                    output_grid[r, c2] = 8

    return output_grid