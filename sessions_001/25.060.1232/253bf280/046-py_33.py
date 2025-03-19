"""
1.  **Identify Azure Pixels:** Locate all azure (8) pixels within the input grid.
2.  **Create Green Cross:** For each azure pixel:
    *   If there is not a green pixel directly above the azure, place green pixel in the grid location directly above it.
    *   Repeat for the locations: below, to the left and to the right.
3.  **Preserve Azure:** Maintain all existing azure pixels in their original locations, unchanged.
4. **Maintain all Zeros:** The black (0) pixels remain as they are.

In other words if there is an object composed of connected azure pixels:

1.  Maintain the initial object pixels.
2.  Expand the shape into a '+' cross like shape by adding green to each branch.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the locations of all azure pixels.
    azure_pixels = np.argwhere(input_grid == 8)

    # Create green pixels around each azure pixel.
    for row, col in azure_pixels:
        # Check and place green pixel above.
        if row > 0 and output_grid[row-1, col] != 3:
            output_grid[row-1, col] = 3
        # Check and place green pixel below.
        if row < rows - 1 and output_grid[row+1, col] != 3:
            output_grid[row+1, col] = 3
        # Check and place green pixel to the left.
        if col > 0 and output_grid[row, col-1] != 3:
            output_grid[row, col-1] = 3
        # Check and place green pixel to the right.
        if col < cols - 1 and output_grid[row, col+1] != 3:
            output_grid[row, col+1] = 3
    return output_grid