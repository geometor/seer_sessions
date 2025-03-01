# 5bd6f4ac • 023 • refine_coder

---
```python
"""
1.  **Input:** A 2D grid of integers (colors).
2.  **Output:** A 3x3 grid of integers.
3.  **Transformation:**
    *   Find the bottom-right non-zero pixel in the entire input grid.
    *   Set the value of the bottom-right cell (index [2, 2]) of the output grid to the value of the found pixel.
    *   All other cells in the output grid are 0.
"""

import numpy as np

def get_bottom_right_nonzero(grid):
    """
    Finds the bottom-right non-zero pixel within the grid.
    Returns coordinates and value or None if no non-zero pixel.
    """
    rows, cols = grid.shape
    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if grid[i, j] != 0:
                return (i, j), grid[i, j]
    return None, 0

def transform(input_grid):
    # Initialize output_grid as 3x3 with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the bottom-right non-zero pixel in the input grid.
    _, value = get_bottom_right_nonzero(input_grid)

    # Set the bottom-right pixel of the output grid to the found value.
    if value:  # check in case the entire input_grid is all zeros.
        output_grid[2, 2] = value

    return output_grid
```
