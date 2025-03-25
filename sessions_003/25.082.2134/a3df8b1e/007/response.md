```python
"""
Transforms an input grid with a single '1' at the bottom row into an output grid with a checkered pattern. The checkerboard pattern's origin is determined by the location of the '1' in the input.
"""

import numpy as np

def find_input_origin(input_grid):
    """Finds the row and column index of the pixel with value 1 in the last row."""
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

    # 1. Find Input Origin: Locate the single blue pixel (value 1) in the last row.
    input_origin_row, input_origin_col = find_input_origin(input_grid)

    # 2. Generate Checkerboard: Create output grid (same dimensions).
    # 3. Determine Pixel Values: Calculate value based on input origin.
    for r in range(rows):
        for c in range(cols):
            # value = (input_origin_row + input_origin_col + current_row + current_col) % 2
            value = (input_origin_row + input_origin_col + r + c) % 2
            output_grid[r, c] = value

    # 4. return the output_grid
    return output_grid
```