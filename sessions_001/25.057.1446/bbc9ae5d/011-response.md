# bbc9ae5d • 011 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all red pixels (value 2) within the input grid.
2.  **Count Red Blocks:** Count the number of contiguous horizontal blocks of red pixels. For instance, `2, 2, 0, 2` has three blocks: `2,2`, `2`.
3.  **Determine output height** Divide the number of blocks by 2, if there is a remainder round up.
4.  **Consolidate:** Create a new output grid. Place the red pixels, maintaining their horizontal contiguity if present in the input, at the beginning of the output grid (leftmost columns).
5.  **Determine output width:** If the height is greater than 1, the width is Input width / Height, otherwise output width is the same as the input.
6.  **Fill Remaining Space:** Fill any remaining cells in the output grid with white pixels (value 0).
"""

import numpy as np
from collections import deque

def count_red_blocks(input_grid):
    """Counts contiguous horizontal blocks of red pixels."""
    grid = np.array(input_grid)
    blocks = 0
    in_block = False
    for x in range(grid.shape[1]):
        if grid[0, x] == 2:
            if not in_block:
                blocks += 1
                in_block = True
        else:
            in_block = False
    return blocks

def get_red_blocks(input_grid):
    """Gets a list of lists containing the red blocks as numpy arrays"""
    grid = np.array(input_grid)
    blocks_list = []
    current_block = []

    for x in range(grid.shape[1]):
        if grid[0,x] == 2:
            current_block.append(2)
        else:
            if len(current_block) > 0:
                blocks_list.append(np.array(current_block))
                current_block = []

    # Check for a block at the very end:
    if len(current_block) > 0:
        blocks_list.append(np.array(current_block))

    return blocks_list


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    num_red_blocks = count_red_blocks(input_grid)
    output_height = (num_red_blocks + 1) // 2 if num_red_blocks > 0 else 0

    if output_height > 1:
        output_width = input_grid.shape[1]
    elif output_height <= 1:
        output_width = input_grid.shape[1]

    if output_height == 0:
        return [[]]  #handle corner case of no red blocks

    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    red_blocks = get_red_blocks(input_grid)
    red_pixels_placed = 0

    
    row = 0
    col = 0
    for block in red_blocks:
        for _ in range(len(block)):
            output_grid[row, col] = 2
            col += 1
            red_pixels_placed +=1
            if col >= output_width:
                col = 0
                row += 1
                if row >= output_height and red_pixels_placed < sum([len(b) for b in red_blocks]):
                  output_grid = np.concatenate((output_grid, np.zeros((1,output_width))),axis=0)
                  output_height += 1
        

    return output_grid
```
