"""
1. **Identify the Core:** Locate the 2x2 block of non-zero pixels within the input grid. This is the "core block". Note the colors and the top-left coordinates of this block.

2. **Mirror/Duplicate:**
   - examine the values in clockwise fashion starting at the top right.
   - top-right value is duplicated in top-left 2x2 of the output
   - bottom-right value is duplicated in top-right 2x2 of the output
   - bottom-left value is duplicated in bottom-right 2x2 of the output
   - top-left value is duplicated in bottom-left 2x2 of the output

3. **Fill Remaining Cells:** Fill all other cells in the output grid with 0 (white/background).
"""

import numpy as np

def find_core_block(grid):
    # Find the 2x2 block of non-zero pixels.
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] != 0 and grid[r, c+1] != 0 and grid[r+1, c] != 0 and grid[r+1, c+1] != 0:
                return r, c
    return None  # Should not happen in valid inputs, based on observations

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    
    # Find core block coordinates
    core_r, core_c = find_core_block(input_grid)

    # Extract core block colors
    top_left = input_grid[core_r, core_c]
    top_right = input_grid[core_r, core_c + 1]
    bottom_right = input_grid[core_r + 1, core_c + 1]
    bottom_left = input_grid[core_r + 1, core_c]
    
    # Duplicate and reflect core block
    # top-right value is duplicated in top-left 2x2
    if rows >= 2 and cols >=2:
        output_grid[0:2, 0:2] = top_right

    # bottom-right value is duplicated in the top-right 2x2    
    if rows >= 2 and cols >= 4:    
        output_grid[0:2, cols-2:] = bottom_right

    # bottom-left is duplicated in bottom-right 2x2
    if rows >=4 and cols >= 4:
        output_grid[rows-2:, cols-2:] = bottom_left
        
    # top-left is duplicated in the bottom-left
    if rows >= 4 and cols >= 2:
        output_grid[rows-2:, 0:2] = top_left

    # place core in the center
    output_grid[core_r, core_c] = input_grid[core_r, core_c]
    output_grid[core_r, core_c+1] = input_grid[core_r, core_c+1]
    output_grid[core_r+1, core_c] = input_grid[core_r+1, core_c]
    output_grid[core_r+1, core_c+1] = input_grid[core_r+1, core_c+1]
    
    return output_grid