# d511f180 • 008 • example_2 • investigate_coder

---
```python
"""
Swap the colors of the top-middle and middle-right cells of a 3x3 grid, keeping other cells unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap the colors of the specified cells.
    # Top-middle cell (0, 1)
    # Middle-right cell (1, 2)
    output_grid[0, 1], output_grid[1, 2] = output_grid[1, 2], output_grid[0, 1]

    return output_grid
```
