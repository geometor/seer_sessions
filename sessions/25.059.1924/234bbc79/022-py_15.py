"""
1.  **Identify and Remove:** Identify all pixels with the color gray (5) and remove them entirely from the grid.
2.  **Retain:** Keep all the occurrences of color blue(1) and red(2)
3. **Resize:** The output grid will be of dimensions 3x8
4. **Result:** Construct the output grid, which is a 3x8 section of the top-left part of the input grid, after removing the gray pixels, ensuring all blues are on the left of all reds.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 8), dtype=int)

    # Filter out gray (5) pixels, retain blue (1) and red (2).
    temp_grid = []
    for r in range(min(rows,3)):
        row_pixels = []
        for c in range(cols):
          if input_grid[r,c] != 5:
            row_pixels.append(input_grid[r,c])
        temp_grid.append(row_pixels)      

    # populate the output grid
    for r in range(min(rows,3)):
      for c in range(min(len(temp_grid[r]),8)):
        output_grid[r,c] = temp_grid[r][c]

    return output_grid.tolist()