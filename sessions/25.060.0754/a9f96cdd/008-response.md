# a9f96cdd • 008 • refine_coder

---
```python
"""
1.  **Identify 2x2 Squares:** Examine the input grid to find all 2x2 squares where all four pixels have the same color.
2.  **Centering Rule**: Of the identified 2x2 squares, only consider one that is "centered" within the input grid.  "Centered" means that if you were to remove the 2x2 square, the remaining pixels could be divided into four groups (top, bottom, left, right) where the number of rows in the top and bottom groups are equal or differ by no more than 1, and the number of columns in the left and right groups are equal or differ by no more than 1.
3. **Prioritization** If there are *multiple* centered 2x2 squares of different colors, select the one appearing first by top to bottom, then left to right location of the 2x2 square.
4.  **Output Grid:** Create a 3x3 output grid.
5.  **Fill Output:** If a centered 2x2 square was found, fill the entire output grid with the color of that square.
6.  **Default Output:** If no centered 2x2 square is found, fill the output grid with white (color 0).
"""

import numpy as np

def find_2x2_squares(grid):
    """Finds all 2x2 squares of the same color in the grid."""
    squares = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            subgrid = grid[r:r+2, c:c+2]
            if np.all(subgrid == subgrid[0, 0]):
                squares.append((r, c, subgrid[0, 0]))  # (row, col, color)
    return squares

def is_centered(square, grid_shape):
    """Checks if a 2x2 square is centered within the grid."""
    r, c, _ = square
    rows, cols = grid_shape
    top_padding = r
    bottom_padding = rows - (r + 2)
    left_padding = c
    right_padding = cols - (c + 2)

    row_diff = abs(top_padding - bottom_padding)
    col_diff = abs(left_padding - right_padding)

    return row_diff <= 1 and col_diff <= 1

def transform(input_grid):
    # Find all 2x2 squares.
    squares = find_2x2_squares(input_grid)

    # Filter for centered squares.
    centered_squares = [
        square for square in squares if is_centered(square, input_grid.shape)
    ]

    # Initialize a 3x3 output grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Prioritize centered squares (top-to-bottom, then left-to-right).
    if centered_squares:
        centered_squares.sort(key=lambda x: (x[0], x[1]))  # Sort by row, then col
        _, _, color = centered_squares[0]
        output_grid[:] = color

    return output_grid
```
