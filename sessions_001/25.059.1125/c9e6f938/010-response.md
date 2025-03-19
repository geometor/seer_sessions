# c9e6f938 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** all orange (7) pixels in the input grid.
2.  **Double** the width of the input grid from 3 to 6 columns, only if the input is 3x3
3.  **For each contiguous block of orange pixels**, duplicate that horizontal block by extending it to the right one time.
4.  **All other** pixels remain unchanged (white stays white).
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    """Finds contiguous horizontal blocks of a given color."""
    blocks = []
    rows, cols = grid.shape
    for r in range(rows):
        in_block = False
        start_col = 0
        for c in range(cols):
            if grid[r, c] == color:
                if not in_block:
                    in_block = True
                    start_col = c
            elif in_block:
                in_block = False
                blocks.append((r, start_col, c - 1))
        if in_block:
            blocks.append((r, start_col, cols - 1))
    return blocks

def transform(input_grid):
    # Double the width of the grid if it's 3x3.
    if input_grid.shape == (3,3):
        output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)
    else:
        return input_grid

    # Copy existing pixels.
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        output_grid[r,c] = input_grid[r,c]

    # Find contiguous blocks of orange (7) pixels.
    orange_blocks = find_contiguous_blocks(input_grid, 7)

    # Duplicate each orange block horizontally.
    for block in orange_blocks:
        row, start_col, end_col = block
        block_length = end_col - start_col + 1
        for i in range(block_length):
          output_grid[row,start_col + block_length + i] = 7

    return output_grid
```
