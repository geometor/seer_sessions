"""
1.  **Identify:** Find all non-zero pixels in the input grid. Each of these is a "seed" pixel.
2.  **Iterate:** For each seed pixel:
3.  **Top Rectangle:** Create a rectangle of the same color as the seed pixel. This rectangle's bottom edge is the row *above* the seed pixel's row. The rectangle extends upwards to the top edge of the grid (row 0). The rectangle extends horizontally to the left and right edges of the grid.
4.  **Bottom Rectangle:** Create another rectangle of the same color. This rectangle's top edge is the row *below* the seed pixel's row. This rectangle extends downwards to the bottom edge of the grid. The rectangle extends horizontally to the left and right edges of the grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Non-Zero Pixels
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((r, c, input_grid[r, c]))

    # 2. Iterate through non-zero pixels
    for r, c, value in non_zero_pixels:
        # 3. Generate Top Rectangle
        for i in range(r):  # Up to the row above the seed
            for j in range(cols): # Extend to all columns
                output_grid[i, j] = value

        # 4. Generate Bottom Rectangle
        for i in range(r + 1, rows):  # From the row below the seed to the bottom
            for j in range(cols): # Extend to all columns
                output_grid[i, j] = value

    return output_grid