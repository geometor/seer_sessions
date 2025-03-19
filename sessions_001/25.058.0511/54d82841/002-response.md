# 54d82841 • 002 • example_1 • investigate_coder

---
```python
"""
Copy the input grid to the output grid. Then, in the last row of the output grid, add yellow pixels in the 3rd and 7th columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Add yellow pixels to the last row at specific columns.
    output_grid[rows - 1, 2] = 4  # 3rd column (index 2)
    output_grid[rows - 1, 6] = 4  # 7th column (index 6)

    return output_grid
```
