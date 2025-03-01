# 1fad071e • 018 • refine_coder

---
```python
"""
The transformation creates a 1xN output grid, where N is determined by the presence and count of uniform color blocks in the input. If the input consists of only 2x2 blue blocks, the output is a 1xN grid of 1s, where N is the number of 2x2 blue blocks. If input consists of all the same non-blue colors, the output is just [[0]]. If the bottom row has any non-blue that is the same as its neighbor, it is ignored.

"""

import numpy as np

def count_2x2_blocks(input_grid):
    """Counts the number of 2x2 blocks of the same color."""
    count = 0
    rows, cols = input_grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            block = input_grid[i:i+2, j:j+2]
            if np.all(block == block[0, 0]) and block[0,0] == 1:
                count += 1
    return count

def transform(input_grid):
    # Count the 2x2 blue blocks.
    counts = count_2x2_blocks(np.array(input_grid))

    input_grid = np.array(input_grid)

    # all same non-blue color
    if np.all(input_grid == input_grid[0,0]) and input_grid[0,0] != 1:
      return np.array([[0]])
    
    # if we have any counts, return a 1xN grid of just ones
    if counts > 0:
      output_grid = np.ones((1, counts), dtype=int)
      return output_grid

    return np.array([[0]])
```
