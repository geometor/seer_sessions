# fcc82909 • 012 • refine_coder

---
```python
"""
1.  **Identify 2x2 Squares:** Examine the input grid to locate all 2x2 squares.
2.  **Check for Distinct Colors:** For each identified 2x2 square, determine the number of distinct colors present.
3.  **Conditional Transformation:** If a 2x2 square contains exactly four distinct colors, replace the entire 2x2 square in the output grid with green (color value 3).
4.  **Preserve Otherwise:** If a 2x2 square does not have four distinct colors, or if a location is not part of such, the output is a copy of the input.
"""

import numpy as np

def find_2x2_squares(grid):
    """Finds all 2x2 squares in the grid."""
    squares = []
    for i in range(grid.shape[0] - 1):
        for j in range(grid.shape[1] - 1):
            squares.append((i, j))
    return squares

def has_distinct_colors(grid, i, j):
    """Checks if a 2x2 square has four distinct colors."""
    square = grid[i:i+2, j:j+2]
    return len(np.unique(square)) == 4

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 squares
    squares = find_2x2_squares(input_grid)

    # Iterate through each 2x2 square
    for i, j in squares:
        # Check if the 2x2 square has four distinct colors
        if has_distinct_colors(input_grid, i, j):
            # Replace the entire 2x2 square with green (color value 3)
            output_grid[i:i+2, j:j+2] = 3

    return output_grid
```
