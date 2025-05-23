```python
"""
1. **Identify 2x2 Green Squares:** Scan the input grid to locate all instances of four green (3) pixels forming a 2x2 square. A 2x2 square is defined by green pixels at positions (r, c), (r, c+1), (r+1, c), and (r+1, c+1) for any row 'r' and column 'c'.

2. **Transform All Pixels in Square:** For *each* 2x2 green square identified, change the color of *all four* pixels within that square from green (3) to azure (8).

3. **Preserve Other Pixels:** All other pixels in the grid that are not part of a 2x2 green square remain unchanged.
"""

import numpy as np

def find_2x2_green_squares(grid):
    """Finds the top-left coordinates of all 2x2 green squares in the grid."""
    squares = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == 3 and
                grid[r, c + 1] == 3 and
                grid[r + 1, c] == 3 and
                grid[r + 1, c + 1] == 3):
                squares.append((r, c))
    return squares

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all 2x2 green squares
    squares = find_2x2_green_squares(output_grid)

    # Change all pixels within each square to 8
    for r, c in squares:
        output_grid[r, c] = 8
        output_grid[r, c + 1] = 8
        output_grid[r + 1, c] = 8
        output_grid[r + 1, c + 1] = 8

    return output_grid
```
