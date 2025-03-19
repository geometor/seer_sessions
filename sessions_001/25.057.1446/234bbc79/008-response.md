# 234bbc79 • 008 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid based on color-specific rules, primarily focusing on
the interaction between vertically adjacent pixels and the influence of the first row.

1. **Initialization:** The output grid starts as a copy of the input grid.
2. **Gray (5) Replacement:** Any gray (5) pixel in the input grid that has a vertically adjacent pixel *directly above* it is replaced with the color blue (1) on the *last* row. These vertical relationships carry from the second to last row, and appear on the last row.
3.  **Blue(1) Addition** Where blue (1) appears in the first row, a series of blue pixels (1) is added to the last row.
4. **Green(3) Addition** Where green appears (3) in the second row, green (3) appears in the last row.
5.  **Preservation of Other Colors:** Colors not mentioned above are preserved in their original positions if there are not interactions.
6. The output grid is the result of those changes.
"""

import numpy as np

def get_vertically_adjacent_below(grid, row, col):
    """Returns the pixel directly below the given cell, or None if at the bottom."""
    if row < grid.shape[0] - 1:
        return grid[row + 1, col]
    return None

def get_vertically_adjacent_above(grid, row, col):
    """Returns the pixel directly above the given cell, or None if at the top."""
    if row > 0:
        return grid[row - 1, col]
    return None

def transform(input_grid):
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    last_row = rows - 1

    for r in range(rows):
       for c in range(cols):
            #Gray(5) to Blue(1) in the last row
            if r == rows - 2 and input_grid[r,c] == 5:
                if get_vertically_adjacent_above(input_grid,r,c) is not None:
                    output_grid[last_row,c] = 1
            if r==0 and input_grid[r,c] == 1:
                output_grid[last_row,c] = 1
            if r == 1 and input_grid[r,c] == 3:
                output_grid[last_row,c] = 3

            if r == last_row: # last row
                # if the original pixel was 5, change it to 1
                if input_grid[r,c] == 5:
                    output_grid[last_row,c] = 1


    return output_grid
```
