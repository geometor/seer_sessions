```python
"""
1.  **Input:** Examine the input grid.
2.  **Identify Regions:** Identify contiguous regions of the same color within the input grid.
3.  **Selection Rule:**
   * The program copies parts of shapes from input into the 3 x 4 output grid.
   * The output grid is a direct copy of *some* parts of the input.
4.  **Output:** Create a 3x4 output grid, copying selected regions from the input grid into the output grid, maintaining their shapes and relative positions as much as possible within the 3x4 bounds. If the copied regions would exceed the 3x4 size, they are truncated.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 4), dtype=int)
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # change output pixels 
    # Iterate through the input grid, copying to the output grid.
    for i in range(min(3, input_height)):
        for j in range(min(4, input_width)):
            output_grid[i, j] = input_grid[i, j]

    return output_grid
```