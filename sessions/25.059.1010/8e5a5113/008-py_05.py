"""
1. **Divide:** The input grid is conceptually divided into two vertical halves.

2.  **Preserve Structure:** The right half of the output grid maintains the same pixel structure (positions of grey and other colors) as the right half of the input grid.

3.  **Gray Pixel Replacement:**
    *   For each gray pixel in the right half of the *input* grid, find the corresponding pixel in the mirrored position on the left half of the *input* grid.
    *   If the mirrored pixel is *not* gray, replace the gray pixel in the *output* grid with the color of the mirrored pixel.

4.  **White Pixel Replacement:**
    *    For each white pixel in the right half of the *input* grid.
    *    scan the *input* grid's left side, from the leftmost column.
    *    Use the first non-gray pixel found on the left side to change the pixel.

5. **Other Colors**
    * If there are other colors than gray or white on the right side, maintain them.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    midpoint = cols // 2

    # Iterate through the right half of the grid
    for r in range(rows):
        for c in range(midpoint, cols):
            # Determine corresponding column on the left side
            left_col = midpoint - (c - midpoint) - 1

            if input_grid[r, c] == 5:  # If gray
                if left_col >= 0 and input_grid[r, left_col] != 5:
                    output_grid[r, c] = input_grid[r, left_col]

            elif input_grid[r, c] == 0:  # If white
                # Find the first non-gray pixel in the row on the left side
                for i in range(midpoint):
                    if input_grid[r, i] != 5:
                        output_grid[r, c] = input_grid[r, i]
                        break

    return output_grid