# 99b1bc43 • 012 • refine_coder

---
```python
"""
Conceptually divide the input grid into non-overlapping 2x2 blocks. For each block:

1.  Check the pattern.
2.  If the pattern is blue on the top left, bottom right, and top right, output the color in the bottom left of the square.
3. If blue is only in a single cell, output is green
4. Else, Output White.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows // 2
    output_cols = cols // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    for i in range(output_rows):
        for j in range(output_cols):
            # Define the 2x2 block in the input grid
            block = input_grid[2*i:2*i+2, 2*j:2*j+2]
            # Check for the specific pattern
            if (block[0, 0] == 1 and block[1, 1] == 1 and block[0, 1] == 1):
                output_grid[i, j] = block[1,0] #output color of bottom left.
            elif np.sum(block == 1) == 1:  # Count occurrences of '1' (blue)
                 output_grid[i,j] = 3
            else:
                output_grid[i, j] = 0  # Set to '0' (white)

    return output_grid.tolist()
```
