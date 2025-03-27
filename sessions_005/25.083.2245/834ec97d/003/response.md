```python
"""
Identifies contiguous regions of non-zero pixels (shapes) in the input grid,
preserves them in the output grid, and adds a border of '4's above each shape
where '0's are present.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Preserve original shape
    for i in range(rows):
        for j in range(cols):
            if input_grid[i][j] != 0:
                output_grid[i][j] = input_grid[i][j]

    # Border Top
    for i in range(rows):
        for j in range(cols):
            # check for '0' in input and non-zero below
            if input_grid[i][j] == 0 and i + 1 < rows and input_grid[i+1][j] != 0:
                output_grid[i][j] = 4

    return output_grid
```
