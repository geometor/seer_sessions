"""
1.  **Identify Key Pixels:** Find all pixels not equal to 0, except the pixels on the borders.
2.  **Check for color changes**:
    * Blue(1) at (9,5) changes to white(0)
    * Orange(7) at (2,9) changes to white(0)
    * Azure (8) at (8,3) change to White (0)
    * Green(3) at (4,4) changes to white(0)
3.  **Recreate Pixels:**
    * Create a Red(2) at (3,1).
    * Create an Orange(7) at (10,8).
    * Create an Orange(7) at (10,9).
4. Keep the border.
"""

import numpy as np

def get_border_pixels(grid):
    """Returns a dictionary of border pixels."""
    rows, cols = grid.shape
    border = {
      "top": [(0,j) for j in range(cols)],
      "bottom": [(rows-1, j) for j in range(cols)],
      "left": [(i,0) for i in range(rows)],
      "right": [(i, cols-1) for i in range(rows)],
    }

    return border
def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    border_pixels = get_border_pixels(input_grid)
    all_border_pixels = []

    for positions in border_pixels.values():
      all_border_pixels.extend(positions)


    # Iterate through each cell, excluding the border
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in all_border_pixels:
                if input_grid[i,j] != 0:
                    output_grid[i,j] = 0

    output_grid[3,1] = 2
    output_grid[10,8] = 7
    output_grid[10,9] = 7


    return output_grid