# 137eaa0f • 016 • example_3 • investigate_coder

---
```python
"""
Extracts all non-zero pixels from a large grid and places them into a smaller grid,
starting from the top-left corner, effectively removing all zero-valued pixels
and condensing the remaining ones.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates and values of all non-zero pixels in a grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple contains (row, column, value)
        of a non-zero pixel.
    """
    nonzero_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append((r, c, grid[r, c]))
    return nonzero_pixels

def transform(input_grid):
    """
    Transforms the input grid by extracting non-zero pixels and arranging
    them in a condensed output grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # 1. Identify Non-Zero Pixels and their locations.
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # 2. Create a new output grid, enough to fit non-zero pixels
    output_grid = np.zeros((len(nonzero_pixels), len(nonzero_pixels)), dtype=int)

    #3. Extract, and Position:
    output_row = 0
    output_col = 0

    for _, _, value in nonzero_pixels:
          output_grid[output_row,output_col] = value
          output_col += 1
          if output_col >= output_grid.shape[1]:
            output_col = 0
            output_row +=1

    #4. Determine the required size, trimming the grid

    #find dimensions needed
    max_row = 0
    max_col = 0

    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] != 0:
          if r > max_row:
            max_row = r
          if c > max_col:
            max_col = c

    trimmed_output_grid = output_grid[:max_row+1,:max_col+1]
    return trimmed_output_grid
```
