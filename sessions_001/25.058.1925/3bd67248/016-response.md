# 3bd67248 • 016 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by:
1. Identifying the leftmost column containing only '8' (azure).
2. Creating a diagonal line of '2' (red) from the top-right to the bottom-left.
3. Replacing the entire bottom row with '4' (yellow).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Create a diagonal of '2's from top-right to bottom-left
    for i in range(rows):
        output_grid[i, cols - 1 - i] = 2

    # Replace the bottom row with '4's
    output_grid[rows - 1, :] = 4

    return output_grid
```
