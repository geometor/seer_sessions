# 77fdfe62 • 016 • example_3 • investigate_coder

---
```python
"""
Divide the 8x8 input grid into sixteen non-overlapping 2x2 subgrids.  For each 2x2 block, get the value of the pixel at the top-left corner of the subgrid and assign this value to the corresponding pixel in the 4x4 output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 4x4 array filled with zeros.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the 2x2 subgrids of the input grid.
    for i in range(4):
        for j in range(4):
            # Extract the top-left pixel value of each 2x2 subgrid.
            output_grid[i, j] = input_grid[i * 2, j * 2]

    return output_grid
```
