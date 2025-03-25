```python
"""
Transforms an input grid with a single '1' at the bottom row into an output grid with a checkered pattern. The checkerboard's origin is derived from the position of the '1' in the input grid.
"""

import numpy as np

def find_input_origin(input_grid):
    """Finds the column index of the leftmost pixel with value 1 in the last row."""
    rows = len(input_grid)
    cols = len(input_grid[0])
    for c in range(cols):
        if input_grid[rows - 1][c] == 1:
            return rows - 1, c
    return None  # Should not happen according to problem description

def transform(input_grid):
    """Transforms the input_grid to a checkered pattern output_grid."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Identify the Input Origin.
    input_origin_row, input_origin_col = find_input_origin(input_grid)

    # 2. Calculate Output Grid Origin Row.
    output_origin_row = input_origin_row - (cols - 1 - input_origin_col)

    # 3. Calculate Output Grid Origin Column (same as input).
    output_origin_col = input_origin_col

    # 4. Checkerboard Generation.
    for r in range(rows):
        for c in range(cols):
            # Calculate value based on origin and current cell coordinates.
            value = (output_origin_row + output_origin_col + r + c) % 2
            output_grid[r, c] = value

    # 5. Return the output_grid.
    return output_grid
```