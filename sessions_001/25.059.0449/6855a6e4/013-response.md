# 6855a6e4 • 013 • refine_coder

---
```python
"""
The transformation involves identifying a 3x3 red block and positioning gray blocks relative to it. The red block remains in its original position.
The gray blocks in the output are created based on the position of the red object, the gray objects are not a transformation of the input grids gray blocks.
"""

import numpy as np

def find_red_block(grid):
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            if (grid[r:r+3, c:c+3] == 2).all():
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the 3x3 red block
    red_block_pos = find_red_block(input_grid)

    # clear any input gray pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 5:
                output_grid[r,c] = 0

    if red_block_pos:
        red_row, red_col = red_block_pos

        # Determine gray block placement based on examples.
        # Surrounding the red block with gray

        # Calculate available space above/below
        space_above = red_row
        space_below = rows - (red_row + 3)
        total_space = space_above + space_below

        if total_space >= 2:
            if space_above >=2 and space_below >=2 :
                # put gray above and below
                gray_top = red_row - 2
                gray_height = 2

                gray_left = red_col - 6
                if gray_left < 0:
                    gray_left = red_col - 5
                if gray_left < 0:
                    gray_left = red_col - 4
                if gray_left < 0:
                    gray_left = red_col - 3
                if gray_left < 0:
                    gray_left = red_col - 2                                                            
                if gray_left < 0:
                    gray_left = red_col - 1
                if gray_left < 0:
                    gray_left = red_col

                gray_width = 10
                if gray_left + gray_width > cols:
                    gray_width = cols - gray_left
                    if gray_width <= 5:
                        # shift grey to center
                        diff =  5 - gray_width
                        gray_left = gray_left - diff
                        gray_width = 10
                #place 2 rows above
                output_grid[gray_top:gray_top + gray_height, gray_left:gray_left+gray_width ] = 5

                gray_bottom = red_row + 3
                #place 2 rows below
                output_grid[gray_bottom:gray_bottom+gray_height, gray_left:gray_left+gray_width ] = 5
            elif total_space > 4:
                # Place gray block around red
                gray_row = red_row - 2
                gray_height = 6 # Two rows above, red block height and two rows below

                output_grid[red_row-1, red_col-1:red_col+4] = 5
                output_grid[red_row, red_col-1] = 5
                output_grid[red_row+1, red_col-1] = 5
                output_grid[red_row+2, red_col-1] = 5
                output_grid[red_row+3, red_col-1:red_col+4] = 5


    return output_grid
```
