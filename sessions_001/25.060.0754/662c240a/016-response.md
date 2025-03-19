# 662c240a • 016 • refine_coder

---
```python
"""
The program extracts a 3x3 sub-grid from the input grid. The sub-grid is
defined as a contiguous 3x3 block of pixels that all have the same color.
"""

import numpy as np

def find_3x3_block(grid):
    """Finds the top-left coordinates of the first 3x3 block of the same color."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r in range(rows - 2):
        for c in range(cols - 2):
            color = grid[r][c]
            is_block = True
            for i in range(3):
                for j in range(3):
                    if grid[r + i][c + j] != color:
                        is_block = False
                        break
                if not is_block:
                    break
            if is_block:
                return r, c
    return None, None  # No 3x3 block found


def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Find the top-left coordinates of a 3x3 block
    start_row, start_col = find_3x3_block(input_array)
    
    # Initialize the output grid (handle case where no block is found).
    output_array = np.zeros((3,3), dtype=int)

    # Extract the 3x3 block if found.
    if start_row is not None and start_col is not None:
        output_array = input_array[start_row:start_row+3, start_col:start_col+3]

    # convert back to list
    output_grid = output_array.tolist()
    return output_grid
```
