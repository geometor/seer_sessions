```python
"""
Transforms an input grid with a single '1' at the bottom row into an output grid with a checkered pattern emanating from the position of the '1'. The checkerboard pattern is determined by the Manhattan distance from the starting '1' pixel.
"""

import numpy as np

def find_starting_pixel(grid):
    """Finds the column index of the pixel with value 1 in the last row."""
    rows = len(grid)
    cols = len(grid[0])
    for c in range(cols):
        if grid[rows - 1][c] == 1:
            return rows - 1, c  # Return row, col
    return None  # Should not happen according to the problem description

def manhattan_distance(row1, col1, row2, col2):
    """Calculates the Manhattan distance between two points."""
    return abs(row1 - row2) + abs(col1 - col2)

def transform(input_grid):
    """
    Transforms the input grid to checkered pattern output grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the starting pixel coordinates (row, col).
    start_row, start_col = find_starting_pixel(input_grid)

   # Generate the checkered pattern.
    for r in range(rows):
        for c in range(cols):
            distance = manhattan_distance(r, c, start_row, start_col)
            if distance % 2 == 0:
                output_grid[r][c] = 1
            else:
                output_grid[r][c] = 0

    return output_grid
```