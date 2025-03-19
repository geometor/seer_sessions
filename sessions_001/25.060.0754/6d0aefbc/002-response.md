# 6d0aefbc • 002 • example_4 • investigate_coder

---
```python
"""
The transformation doubles the width of the input grid and mirrors the original input onto the new grid.
"""

import numpy as np

def transform(input_grid):
    # Get Dimensions of input
    height = len(input_grid)
    width = len(input_grid[0])

    # Create Output Grid: double the width
    output_grid = np.zeros((height, width * 2), dtype=int)

    # Mirror and Copy:
    for row in range(height):
        for col in range(width):
            # Copy to left side
            output_grid[row, col] = input_grid[row, col]
            # Mirror to right side.
            output_grid[row, 2 * width - 1 - col] = input_grid[row, col]

    return output_grid
```
