```python
"""
1. Identify Seed Pixels: Locate all pixels in the input grid with a non-zero value. These are the seed pixels.
2. Horizontal Extension: For each seed pixel, change the color of all pixels to its right, within the same row, to match the seed pixel's color. This extension continues to the right edge of the grid.
3. Vertical Extension: After the horizontal extension is complete for a seed pixel, identify the rightmost pixel of that horizontal extension.  Extend the color of *this* pixel downwards, to all pixels below it in the same column.  This continues to the bottom edge of the grid. Repeat this vertical extension for all horizontal extensions.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell to find seed pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:  # Seed pixel found
                # Horizontal Extension
                for k in range(j, cols):
                    output_grid[i][k] = input_grid[i][j]

    # Iterate through each cell again to apply vertical extension based on the horizontally extended pixels.
    for i in range(rows):
        for j in range(cols):
          if input_grid[i][j] !=0:
            #find rightmost
            for k in range(cols -1, j-1, -1):
              if output_grid[i][k] != 0:
                # Vertical Extension (from the rightmost pixel of the horizontal extension)
                for r in range(i + 1, rows):
                    output_grid[r][k] = output_grid[i][k]
                break;


    return output_grid
```