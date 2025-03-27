"""
1.  **Anti-Diagonal Mirroring:** Create an output grid that is the mirror image of the input grid. The mirroring is performed along the anti-diagonal (top-right to bottom-left). This means the element at input[r][c] will be placed at output[c][r].

2.  **Conditional Recoloring (Based on Input):** *After* placing the mirrored pixel in the output grid, apply a color transformation *based on the original input grid's color* at position [r][c].
    *   If the *input* pixel at [r][c] was red (2), the *output* pixel at [c][r] becomes yellow (4).
    *   If the *input* pixel at [r][c] was green (3), the *output* pixel at [c][r] becomes blue (1).
    *   If the *input* pixel at [r][c] was grey (5), the *output* pixel at [c][r] becomes magenta (6).
    *   If the *input* pixel at [r][c] was magenta (6), the *output* pixel at [c][r] becomes white (0).

3.  **Default Color Preservation:** If an input pixel's color at [r][c] is not part of the specific color transformation rules (i.e., not 2, 3, 5 or 6), then the output pixel at [c][r] retains the *original* color from the mirrored position.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)

    # Mirror along the anti-diagonal and apply recoloring.
    for r in range(rows):
        for c in range(cols):
            # Mirror: Place input[r][c] at output[c][r].
            output_grid[c, r] = input_grid[r, c]

            # Recolor based on the *original* input color.
            if input_grid[r, c] == 2:  # Red to Yellow
                output_grid[c, r] = 4
            elif input_grid[r, c] == 3:  # Green to Blue
                output_grid[c, r] = 1
            elif input_grid[r, c] == 5:  # Grey to Magenta
                output_grid[c, r] = 6
            elif input_grid[r, c] == 6:  # Magenta to White
                output_grid[c, r] = 0

    return output_grid.tolist()