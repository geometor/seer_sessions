# 3c9b0459 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation performs a reflection of the grid across the main diagonal (top-left to bottom-right) combined with a swap.

1.  First swap element at `grid[0][1]` with element at `grid[1][0]`
2.  Then, the grid is reflected along its main diagonal. This means the element at `grid[i][j]` is swapped with the element at `grid[j][i]`.

In simpler way:

The rows of the input grid appear to become the columns of the output grid, and the columns of input grid appear to become the rows in the output grid, but with elements at `grid[0][1]` with element at `grid[1][0]` being swapped.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Swap elements at [0][1] and [1][0]
    temp = output_grid[0][1]
    output_grid[0][1] = output_grid[1][0]
    output_grid[1][0] = temp    

    # Transpose the grid (reflect across the main diagonal)
    output_grid = np.transpose(output_grid)
    
    return output_grid
```
