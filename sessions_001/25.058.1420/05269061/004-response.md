# 05269061 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule involves identifying a seed pattern in the top-left corner of the input grid (non-zero values) and propagating this pattern across the entire output grid. The seed pattern is a 3x3 block. The 0 values in the original input seed get replaced by the repeating sequence from the input grid's first row '2 8 3'.
"""

import numpy as np

def get_seed(grid):
    """Extracts the 3x3 seed pattern from the input grid."""
    return grid[:3, :3].copy()

def fill_seed(seed):
    """
    Completes the seed, filling the 0 with
    the repeating sequence 2,8,3
    """
    top_row = seed[0,:]
    top_row_non_zero = top_row[top_row != 0]
    
    for i in range(3):
        for j in range(3):
          if seed[i,j] == 0:
            seed[i,j] = top_row_non_zero[(i+j) % len(top_row_non_zero)] # alternate through

    return seed

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Get and complete the seed pattern.
    seed = get_seed(input_grid)
    completed_seed = fill_seed(seed)

    # 2. Propagate the seed pattern across the output grid.
    for i in range(rows):
        for j in range(cols):
            output_grid[i, j] = completed_seed[i % 3, j % 3]

    return output_grid.tolist()
```
