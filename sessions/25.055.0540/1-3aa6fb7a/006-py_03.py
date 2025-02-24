"""
1.  **Scan Rows:** Iterate through the grid rows from top to bottom (starting at row 0).
2.  **Find Azure Pixels:** In each row, iterate through the pixels from left to right.
3. **First Azure Pixel is Target**: Locate any azure pixel.
4. **Change to Blue:** If found, change it to blue and stop.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Iterate through rows from top to bottom. Within each row, iterate from
    left to right.  If an azure (8) pixel is found, change it to blue (1)
    and stop processing.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 8:
                output_grid[r, c] = 1
                return output_grid  # Stop after the first change

    return output_grid