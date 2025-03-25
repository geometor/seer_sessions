```python
"""
1. Identify Source Pattern: Find a rectangular block at the top-left corner of the input grid. In the first example it's a 3x3 and the second a 3x4, it may vary in later examples.
2. Identify Target Blocks: Find all rectangular blocks of the same dimension and filled with 5's.
3. Replicate: Copy the source pattern onto each of the target blocks, replacing their contents.
"""

import numpy as np

def find_top_left_pattern(grid):
    """
    Finds the dimensions of a rectangular block at the top-left corner.
    For this problem it is assumed, that the block has non-zero values.
    """
    rows, cols = grid.shape
    
    # Find height by checking when the first 0 is encountered
    height = 0
    for i in range(rows):
      if grid[i,0] == 0:
        break
      height = i + 1

    # Find width by checking when the first 0 is encountered
    width = 0
    for j in range(cols):
      if grid[0,j] == 0:
        break
      width = j+1    

    return grid[:height, :width]

def find_target_blocks(grid, pattern_shape):
    """
    Finds rectangular blocks filled with 5s that match the pattern's dimensions.
    """
    target_blocks = []
    rows, cols = grid.shape
    pattern_height, pattern_width = pattern_shape

    for i in range(rows - pattern_height + 1):
        for j in range(cols - pattern_width + 1):
            block = grid[i:i+pattern_height, j:j+pattern_width]
            if np.all(block == 5):
                target_blocks.append((i, j))
    return target_blocks

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the source pattern at the top-left.
    top_left_pattern = find_top_left_pattern(input_grid)
    pattern_height, pattern_width = top_left_pattern.shape

    # Find target blocks that match the pattern's dimensions and are filled with 5s.
    target_blocks = find_target_blocks(input_grid, top_left_pattern.shape)

    # Replicate the pattern onto each target block.
    for i, j in target_blocks:
        output_grid[i:i+pattern_height, j:j+pattern_width] = top_left_pattern

    return output_grid
```
