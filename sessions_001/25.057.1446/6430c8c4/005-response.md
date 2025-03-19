# 6430c8c4 • 005 • refine_coder

---
```python
"""
1.  Identify Objects: Find all 2x2 blocks of orange (7) pixels within the input grid. Identify all white pixels adjacent to a 2x2 orange block.

2. Transformations
    -   Replace each identified 2x2 orange block with a 2x2 green (3) block in the output grid.
    -   Replace each identified white cell adjacent to a 2x2 orange block with a white (0) in the output grid.
    -   All other pixels in the input grid should retain their original color and position in the output grid.

3.  Output: The output grid has the same dimensions as the input grid.
"""

import numpy as np

def find_orange_blocks(grid):
    """Finds all 2x2 blocks of orange (7) pixels."""
    orange_blocks = []
    for row in range(grid.shape[0] - 1):
        for col in range(grid.shape[1] - 1):
            if np.all(grid[row:row+2, col:col+2] == 7):
                orange_blocks.append((row, col))
    return orange_blocks

def find_adjacent_whites(grid, orange_blocks):
    """Finds all white (1) pixels adjacent to the given orange blocks."""
    white_pixels = set()
    for row, col in orange_blocks:
        # Check above
        if row > 0:
            if grid[row-1, col] == 1:
                white_pixels.add((row - 1, col))
            if grid[row-1, col+1] == 1:
                white_pixels.add((row-1, col+1))

        # Check below
        if row < grid.shape[0] - 2:
            if grid[row+2, col] == 1:
                white_pixels.add((row+2, col))
            if grid[row+2, col+1] == 1:
                 white_pixels.add((row+2, col+1))
        # Check left
        if col > 0:
             if grid[row, col-1] == 1:
                white_pixels.add((row, col-1))
             if grid[row+1, col-1] == 1:
                white_pixels.add((row+1, col-1))

        # Check right
        if col < grid.shape[1] - 2:
            if grid[row, col+2] == 1:
                 white_pixels.add((row, col+2))
            if grid[row+1, col+2] == 1:
                white_pixels.add((row+1, col+2))
    return list(white_pixels)

def transform(input_grid):
    # Initialize output grid with the same dimensions and values as the input
    output_grid = input_grid.copy()

    # Find all 2x2 orange blocks
    orange_blocks = find_orange_blocks(input_grid)

    # Replace orange blocks with green blocks
    for row, col in orange_blocks:
        output_grid[row:row+2, col:col+2] = 3

    #Find white pixels adjacent to orange blocks
    adjacent_whites = find_adjacent_whites(input_grid, orange_blocks)

    # Replace adjacent white pixels with 0
    for row, col in adjacent_whites:
        output_grid[row,col] = 0

    return output_grid
```
