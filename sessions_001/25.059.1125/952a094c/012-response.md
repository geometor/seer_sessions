# 952a094c • 012 • refine_coder

---
```python
"""
The transformation involves rearranging the positions of exactly four specific pixels within the grid. The colors of these pixels are swapped, but no new colors are introduced or removed.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the positions of the four pixels that change.  These are consistent across all examples.
    # These positions are RELATIVE to the overall size of the grid.
    pos1 = (1, 1)
    pos2 = (1, cols - 2)
    pos3 = (rows - 2, 1)
    pos4 = (rows - 2, cols - 2)

    # Perform the swaps. This is a direct permutation of the four pixels.
    output_grid[pos1] = input_grid[pos2]
    output_grid[pos2] = input_grid[pos4]
    output_grid[pos4] = input_grid[pos3]
    output_grid[pos3] = input_grid[pos1]
    
    return output_grid
```
