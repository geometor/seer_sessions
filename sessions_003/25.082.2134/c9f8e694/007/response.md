```python
"""
Iterate through each row of the grid. Within each row, identify "color blocks". A color block is defined as a contiguous sequence of pixels with the same non-zero color, or a sequence of one or more zero-colored pixels. For each non-zero color block: Propagate the color of the block to the right, overwriting any subsequent zero or non-zero pixels. Stop propagation when encountering a pixel that has the same color as the propagating color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by propagating the color of each non-zero color block to the right.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for row in range(rows):
        # Iterate through the row to find color blocks and propagate
        col = 0
        while col < cols:
            if output_grid[row, col] != 0:
                # Found a non-zero color block, start propagation
                start_col = col
                color = output_grid[row, col]

                # Find the end of the current color block, and then propagate
                while col < cols and output_grid[row,col] == color:
                    col += 1
                
                # now propagate
                while col < cols and output_grid[row,col] != color:
                    output_grid[row,col] = color
                    col += 1
            else:
                col += 1 # skip zeros


    return output_grid
```