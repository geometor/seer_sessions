# 1f876c06 • 002 • example_3 • investigate_coder

---
```python
"""
Non-zero pixels in the input grid are replicated vertically downwards, filling their respective columns.
The replication stops when it reaches the bottom of the grid or another non-zero pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating non-zero pixels vertically downwards.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [row[:] for row in input_grid]  # Initialize output_grid as a copy

    # Iterate through each cell in the input grid
    for j in range(cols):
        for i in range(rows):
            if input_grid[i][j] != 0:
                # Replicate the non-zero pixel downwards
                for k in range(i, rows):
                    if output_grid[k][j] == 0 :
                       output_grid[k][j] = input_grid[i][j]
                    else:
                        output_grid[k][j] = input_grid[i][j]
                
    return output_grid
```
