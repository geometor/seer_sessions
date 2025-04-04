# 6430c8c4 • 014 • example_3 • investigate_coder

---
```python
"""
Transforms the input grid into a smaller output grid based on the presence and arrangement of 2x2 blocks of the same non-white color. Each 2x2 block of a non-white color in the input is represented by a single green (3) pixel in the output. The output grid's dimensions are 4x4.
"""

import numpy as np

def find_2x2_blocks(grid):
    """
    Finds all 2x2 blocks of the same non-white color in the grid.
    Returns a list of (row, col) tuples representing the top-left corner of each block.
    """
    blocks = []
    rows, cols = len(grid), len(grid[0])
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r][c] != 0 and \
               grid[r][c] == grid[r+1][c] == grid[r][c+1] == grid[r+1][c+1]:
                blocks.append((r, c))
    return blocks

def transform(input_grid):
    """
    Transforms the input grid into a 4x4 output grid.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation

    # Initialize the output grid with all zeros (white)
    output_grid = np.zeros((4, 4), dtype=int)

    # Find all 2x2 blocks of the same non-white color
    blocks = find_2x2_blocks(input_grid)

    # For each 2x2 block found, set the corresponding pixel in the output grid to green (3)
    for r, c in blocks:
        # Map input grid coordinates to output grid coordinates.  Since we want to inspect
        # the top section, we use mod 4 to map it.
        output_row = r % 4
        output_col = c % 4

        output_grid[output_row][output_col] = 3

    return output_grid.tolist()
```
