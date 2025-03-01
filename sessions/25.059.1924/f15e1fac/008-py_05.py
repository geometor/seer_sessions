"""
1.  **Identify Azure Pixels:** Locate all azure (8) pixels in the input grid.

2.  **Column-wise Processing:** Iterate through each *column* of the grid.

3.  **Azure Extension:** For each column:
    *   Find the *lowest* azure (8) pixel within that column.
    *   Extend that azure pixel downwards to the bottom of the grid, replacing any other colors (except the influencer, if one is stationary).

4. Preserve Red: Ensure the final output retains any red pixels from the original input.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for c in range(cols):
        # Find the lowest azure pixel in the current column
        azure_indices = [row_index for row_index in range(rows) if input_grid[row_index, c] == 8]
        if azure_indices:
            lowest_azure = max(azure_indices)
            # Extend the lowest azure pixel downwards
            for r in range(lowest_azure + 1, rows):
                output_grid[r, c] = 8

    return output_grid