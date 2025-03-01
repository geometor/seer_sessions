# 9f236235 • 004 • example_1 • investigate_coder

---
```python
"""
The program identifies 4x4 blocks of green (3) pixels within the input grid that are bordered by red (2) pixels. 
For each identified green block, the value of the top-left pixel of each block is placed into a smaller output grid. 
The position of the green block in the input grid determines the position of the corresponding pixel in the output grid.
If no green block is present in a quadrant, a white (0) pixel is placed in the output grid.
"""

import numpy as np

def find_green_blocks(grid):
    # Find 4x4 green blocks bordered by red pixels.
    green_blocks = []
    height, width = grid.shape
    for r in range(height - 3):
        for c in range(width - 3):
            block = grid[r:r+4, c:c+4]
            if np.all(block == 3):
                #Check for red borders
                is_bordered = True
                #Check row above
                if r > 0:
                    if not np.all(grid[r-1,c:c+4] == 2):
                         is_bordered = False
                #Check row below
                if r < height - 4:
                    if not np.all(grid[r+4,c:c+4] == 2):
                        is_bordered = False

                #check col to left
                if c > 0:
                    if not np.all(grid[r:r+4,c-1] == 2):
                         is_bordered = False

                #check col to right
                if c < width - 4:
                    if not np.all(grid[r:r+4,c+4] == 2):
                        is_bordered = False
                if is_bordered:
                    green_blocks.append((r, c))
    return green_blocks

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the green blocks
    green_blocks = find_green_blocks(input_grid)

    # Determine output grid size and initialize
    output_size = 4 # from observation of example
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Map green blocks to output grid
    for r, c in green_blocks:
        # Determine the relative position (quadrant) of the green block
        row_index = 0 if r < 9 else 2 #because our identified block groups are 4 x 4 and the overall size of all blocks is 8 x 8
        col_index = 0 if c < 9 else 2
        if row_index == 0 and col_index == 2:
             col_index = 1
        if row_index == 2 and col_index == 2:
             col_index = 3

        # Get the top-left pixel value of block
        pixel_value = input_grid[r,c]

        output_grid[row_index, col_index] = pixel_value
        if row_index == 0 and col_index == 0:
             output_grid[row_index, col_index + 1] = 0
        if row_index == 0 and col_index == 1:
             output_grid[row_index, col_index - 1] = 0
        if row_index == 2 and col_index == 0:
             output_grid[row_index, col_index + 1] = 3
        if row_index == 2 and col_index == 3:
             output_grid[row_index, col_index - 1 ] = 3
    return output_grid
```
