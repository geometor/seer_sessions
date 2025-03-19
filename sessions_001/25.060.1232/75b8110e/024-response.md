# 75b8110e • 024 • refine_coder

---
```python
"""
The transformation extracts a 4x4 subgrid containing a diagonal of non-zero pixels, starting from the bottom-rightmost non-zero pixel and extending diagonally upwards and to the left. If a full 4x4 diagonal cannot be formed, a smaller diagonal subgrid is extracted, maintaining the bottom-right to top-left diagonal characteristic.
"""

import numpy as np

def find_bottom_right_nonzero(grid):
    """Finds the coordinates of the bottom-rightmost non-zero pixel."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] != 0:
                return r, c
    return None  # Return None if no non-zero pixel is found

def transform(input_grid):
    # initialize input_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # find start of diagonal
    start_row, start_col = find_bottom_right_nonzero(input_grid)

    # handle cases where there is no non-zero pixel
    if start_row is None:
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    # determine dimensions of diagonal
    diag_len = min(start_row + 1, start_col + 1, 4) # cannot exceed 4

    # initialize output grid
    output_grid = np.zeros((4, 4), dtype=int)

    # copy diagonal to output
    for i in range(diag_len):
        output_grid[diag_len - 1 - i, i] = input_grid[start_row - i, start_col - i]

    return output_grid.tolist()
```
