# a85d4709 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Initialization:** Start with a 3x3 input grid.
2.  **Substitution:** For each cell in the input grid:
    *   If the cell's value is 0 (white), replace it with 3 (green).
    *   If the cell's value is 5 (gray), replace it with 4 (yellow).
    *   If the cell has any other value, replace it by 2 (red).
3.  **Output:** The result is the transformed 3x3 grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change output pixels based on the substitution rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 4
            else:
                output_grid[i, j] = 2

    return output_grid
```
