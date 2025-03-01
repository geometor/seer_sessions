"""
1.  **Identify colored pixels:** Locate all pixels in the input grid that are not white (0).
2.  **Horizontal Expansion:** For each colored pixel, expand it horizontally to the left and right edges of the grid, changing all pixels in that row to the color of the original pixel.
3.  **Vertical Expansion:** after the row expansion, expand each colored pixel downwards until each column is occupied.

In other words. For the row that a colored object is in, replace the entire row
with the color. Then take each column and fill downwards until you hit the
bottom of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify colored pixels and perform horizontal expansion
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != 0:
                color = output_grid[r, c]
                output_grid[r, :] = color  # Fill entire row with the color

    # Vertical Expansion downwards
    for c in range(cols):
      for r in range(rows):
        if output_grid[r,c] != 0:
          color = output_grid[r,c]
          for r_below in range(r+1, rows):
            output_grid[r_below, c] = color

    return output_grid