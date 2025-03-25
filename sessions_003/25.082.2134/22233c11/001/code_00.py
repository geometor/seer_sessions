"""
The function identifies all green (3) pixels within the input grid. For each green pixel,
it mirrors its position across both diagonal axes. In the output grid,
it places an azure (8) pixel at the mirrored positions. The original green pixels
remain, and all other cells stay white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring green pixels diagonally and
    placing azure pixels at the mirrored positions.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through the grid to find green pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                # Mirror across the main diagonal (top-left to bottom-right)
                mirrored_r1 = c
                mirrored_c1 = r
                if 0 <= mirrored_r1 < rows and 0 <= mirrored_c1 < cols:
                    if output_grid[mirrored_r1, mirrored_c1] == 0:
                        output_grid[mirrored_r1, mirrored_c1] = 8

                # Mirror across the anti-diagonal (top-right to bottom-left)
                mirrored_r2 = cols - 1 - c
                mirrored_c2 = rows - 1 - r
                if 0 <= mirrored_r2 < rows and 0 <= mirrored_c2 < cols:
                    if output_grid[mirrored_r2, mirrored_c2] == 0:
                       output_grid[mirrored_r2, mirrored_c2] = 8

    return output_grid