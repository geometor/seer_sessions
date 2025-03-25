"""
The grid is composed of azure (8) and yellow (4) pixels. The transformation operates on the top three rows (0-2) of the grid. The bottom three rows (3-5) remain unchanged. Within each of the top three rows, azure pixels are filled from the opposite position relative to a central vertical axis (column index 4).
Specifically, if an azure exists on the left side, starting from the reflection point, the right side fills with azure pixels from right to left until an existing azure pixel is hit.
"""

import numpy as np

def reflect_and_fill(row):
    """Fills azure pixels in a single row based on a reflection-like rule across the center column (index 4)."""
    n = len(row)
    new_row = np.copy(row)  # Initialize with the original row
    center = n // 2

    for i in range(center):
        if row[i] == 8:
            for j in range(n - 1 - i, center -1, -1):
                if new_row[j] == 0:
                    new_row[j] = 8
                else:
                    break # Stop if the reflection area contains non zero values

    for i in range(center, n):
       if row[i] == 8:
          for j in range(n-1-i, center, -1):
                if new_row[j] == 0:
                    new_row[j] = 8
                else:
                   break

    return new_row

def transform(input_grid):
    """Transforms the input grid according to the reflection and filling rule."""

    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid

    # Apply transformation to the top three rows only
    for row_index in range(3):
        output_grid[row_index] = reflect_and_fill(input_grid[row_index])

    # Bottom three rows remain unchanged (already copied)
    return output_grid