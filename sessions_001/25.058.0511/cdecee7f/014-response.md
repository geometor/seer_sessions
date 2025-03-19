# cdecee7f • 014 • example_3 • investigate_coder

---
```python
"""
Extracts all non-zero (colored) pixels from a 10x10 input grid and arranges them into a 3x3 output grid.
The order of pixels in the output grid is determined by reading the input grid from bottom-left to top-right.
"""

import numpy as np

def get_nonzero_pixels(grid):
    """
    Extracts the non-zero pixels from the input grid and returns them in a list.
    Reads from the input grid from bottom to top, and left to right.
    """
    nonzero_pixels = []
    for r in range(grid.shape[0] -1, -1, -1):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_pixels.append(grid[r, c])
    return nonzero_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Extract non-zero pixels
    nonzero_pixels = get_nonzero_pixels(np.array(input_grid))

    # Fill the output grid
    k=0
    for i in range(3):
        for j in range(3):
            if k < len(nonzero_pixels):
               output_grid[i,j] = nonzero_pixels[k]
               k+=1

    return output_grid
```
