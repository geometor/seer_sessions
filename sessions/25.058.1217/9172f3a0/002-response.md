# 9172f3a0 • 002 • example_2 • investigate_coder

---
```python
"""
Expands a 3x3 input grid into a 9x9 output grid by replicating each pixel into a 3x3 block.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 9x9 output grid.  Each pixel in the
    input grid is expanded into a 3x3 block of the same color in the output
    grid.  Remaining cells are filled with 0 (white).
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through each pixel in the input grid
    for i in range(3):
        for j in range(3):
            color = input_grid[i, j]
            # Create a 3x3 block in the output grid
            for x in range(3):
                for y in range(3):
                    output_grid[i*3 + x, j*3 + y] = color

    return output_grid
```
