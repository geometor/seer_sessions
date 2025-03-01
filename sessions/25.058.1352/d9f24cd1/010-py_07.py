"""
1.  **Locate Gray Pixels:** Identify all gray (5) pixels within the input grid.
2.  **Fill Gray Column:** For each gray pixel, fill the entire column it occupies with red (2).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with all red (2).
    output_grid = np.full(input_grid.shape, 2)
    rows, cols = output_grid.shape

    # Iterate through the input grid to find gray pixels.
    for r in range(rows):
      for c in range(cols):
        # If a gray pixel is found, keep it gray in the output grid.
        if input_grid[r,c] == 5:
          output_grid[r,c] = 5

    return output_grid