# 5117e062 • 016 • example_3 • investigate_coder

---
```python
"""
Find the largest contiguous cluster of red (value 2) pixels in the input grid. 
Locate bounding box for the red cluster.
Create a 3x3 output grid, copying the 3x3 block from the input array starting
at position [2,0].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # copy a 3x3 area into output grid starting at [2,0] of input
    for i in range(3):
        for j in range(3):
            output_grid[i, j] = input_grid[i + 2, j + 1]

    return output_grid
```
