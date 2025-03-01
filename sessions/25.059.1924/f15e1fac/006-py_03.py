"""
Transformation Rule:

1. **Identify Azure and Red Pixels:** Locate all azure (8) and red (2) pixels in the input grid.

2. **Row-wise Processing:** Iterate through each row of the grid.

3. **Conditional Azure Extension:**
    *   If a row contains at least one red (2) pixel: Extend *all* azure (8) pixels in that row downwards to the bottom of the grid.
    *   If a row does *not* contain any red (2) pixels: Find the lowest azure (8) pixel in each column and extend it downwards to the bottom of the grid.  Other azure pixels in these columns *not* in red-containing rows are *not* extended.

4. **Preserve Red**: Red Pixels remain in place, regardless of the changes.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        row_has_red = False
        for c in range(cols):
            if input_grid[r, c] == 2:
                row_has_red = True
                break

        if row_has_red:
            # Extend all azure pixels in this row downwards
            for c in range(cols):
                if input_grid[r, c] == 8:
                    for r_below in range(r + 1, rows):
                        output_grid[r_below, c] = 8
        else:
            # Extend only the lowest azure pixel in each column downwards
            for c in range(cols):
                azure_indices = [row_index for row_index in range(r, rows) if input_grid[row_index, c] == 8]
                if azure_indices:
                    lowest_azure = max(azure_indices)
                    for r_below in range(lowest_azure + 1, rows):
                        output_grid[r_below, c] = 8
    return output_grid