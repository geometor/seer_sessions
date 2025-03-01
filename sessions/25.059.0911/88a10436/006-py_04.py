"""
1.  **Identify:** Locate any pixels in the input grid that have the value 5 (`pixel_1`).
2.  **Remove:** Remove any pixels of color 5 (`pixel_1`) from the grid.
3. **Output**: Generate the output grid with only the non-5 pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by removing pixels of color 5."""

    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Create an output grid initialized with zeros, same size as input
    output_grid = np.zeros_like(grid)

    # Iterate through the grid and copy only non-5 pixels to output_grid
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 5:
                output_grid[r, c] = grid[r, c]

    # check if output_grid is empty, which happens when the input has size 1x1 and value is 5
    if output_grid.size == 1 and output_grid[0,0] == 0:
      return []

    return output_grid.tolist()