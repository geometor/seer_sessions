```python
"""
1.  **Identify Seed Pixels:** Locate all pixels with non-zero values within the input grid. These are the "seed" pixels.
2.  **Propagation Rule:**
    *   Each seed pixel's value propagates to fill cells *below* it in the same column and *to the right* of it in the same row.
    *   The values do not combine like a logical OR, instead they propagate independently.
3. **Output:** Construct a new grid where the original seed pixels retain their values, and cells below and to the right of each seed are filled with the seed's value.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Finds the coordinates of all non-zero pixels in the grid.
    """
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # get non-zero pixels
    nonzero_pixels = get_nonzero_pixels(input_grid)

    # if no non-zero pixels, return original grid
    if not nonzero_pixels:
      return output_grid

    # propagate values down and right
    for r, c in nonzero_pixels:
        val = input_grid[r,c]
        # Propagate down
        for i in range(r + 1, height):
            output_grid[i, c] = val
        # Propagate right
        for j in range(c + 1, width):
            output_grid[r, j] = val

    return output_grid
```
