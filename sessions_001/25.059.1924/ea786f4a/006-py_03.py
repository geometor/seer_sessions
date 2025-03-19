"""
1.  **Identify the Center:** Locate the central pixel of the input grid (rows // 2, cols // 2).
2.  **Preserve Center Color:** The color of the central pixel in the output grid is the same as its color in the input grid.
3.  **Surrounding Pixels:** For every other pixel:
    *   If the surrounding pixel is in the same row or column as the central pixel, and immediately adjacent, it should be 1 if its row + col is odd or 0 if its row + col is even.
    * If the surrounding pixel is not adjacent to the center, then it should alternate 0, 1 based on if row+col is even.
    * If the surrounding pixel is the same color as a neighboring pixel that is not the center, change it.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Preserve Center
    center_row = rows // 2
    center_col = cols // 2
    output_grid[center_row, center_col] = input_grid[center_row][center_col]

    # Surrounding Pixels
    for i in range(rows):
        for j in range(cols):
            if (i, j) != (center_row, center_col):  # Skip the center pixel
                # Check if adjacent to center
                if (i == center_row and abs(j - center_col) == 1) or \
                   (j == center_col and abs(i - center_row) == 1):
                    output_grid[i, j] = 1 if (i + j) % 2 != 0 else 0
                else:
                     output_grid[i,j] = 1 if (i + j) % 2 != 0 else 0

    return output_grid