```python
"""
1. Identify the Source Pattern: Find the largest contiguous, non-zero rectangular block starting at the top-left corner of the input grid. This is the source pattern.
2. Identify Target Blocks: Find all rectangular blocks within the grid that have the *same dimensions* as the source pattern.
3. Replicate: Copy the source pattern onto each of the identified target blocks, replacing the existing contents.
"""

import numpy as np

def find_top_left_pattern(grid):
    """
    Finds the dimensions of a rectangular block at the top-left corner.
    Assumes that the block is contiguous and has non-zero values (except if the top-left is 0).
    """
    rows, cols = grid.shape

    # Handle edge case where the top-left corner itself is 0.
    if grid[0, 0] == 0:
        return grid[:1,:1]

    
    # Find height
    height = 0
    width = 0
    for i in range(rows):
        if all(grid[i,j] == 0 for j in range(cols) if grid[0,0] != 0 and j < cols):
            break

        # find width for this row:
        row_width = 0
        for j in range(cols):
            if grid[i,j] == 0 and grid[0,0] != 0:
              break
            row_width = j+1
        

        if i>0 and row_width != width:
            break
        
        height = i + 1
        width = row_width
        

    return grid[:height, :width]

def find_target_blocks(grid, pattern_shape):
    """
    Finds rectangular blocks that match the pattern's dimensions.
    """
    target_blocks = []
    rows, cols = grid.shape
    pattern_height, pattern_width = pattern_shape

    for i in range(rows - pattern_height + 1):
        for j in range(cols - pattern_width + 1):
            target_blocks.append((i, j))  # Add all possible blocks
    return target_blocks

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the source pattern at the top-left.
    top_left_pattern = find_top_left_pattern(input_grid)
    pattern_height, pattern_width = top_left_pattern.shape

    # Find all possible target blocks that match the pattern's dimensions.
    target_blocks = find_target_blocks(input_grid, top_left_pattern.shape)

    # Replicate the pattern onto each target block.
    for i, j in target_blocks:
        output_grid[i:i+pattern_height, j:j+pattern_width] = top_left_pattern

    return output_grid
```
