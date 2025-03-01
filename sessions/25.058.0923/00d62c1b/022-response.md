# 00d62c1b • 022 • refine_coder

---
```python
"""
The transformation identifies 2x2 blocks of contiguous green pixels within the input grid.
Within these blocks, only the top-left green pixel is changed to yellow. If no 2x2 green blocks are present, no change is made.
"""

import numpy as np

def find_2x2_green_blocks(grid):
    """
    Finds the top-left coordinates of all 2x2 green blocks in the grid.
    """
    blocks = []
    for row in range(grid.shape[0] - 1):
        for col in range(grid.shape[1] - 1):
            if (grid[row, col] == 3 and
                grid[row + 1, col] == 3 and
                grid[row, col + 1] == 3 and
                grid[row + 1, col + 1] == 3):
                blocks.append((row, col))
    return blocks

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 green blocks
    green_blocks = find_2x2_green_blocks(output_grid)

    # change output pixels 
    for row, col in green_blocks:
        # Change the top-left pixel of each block to yellow
        output_grid[row, col] = 4

    return output_grid
```
