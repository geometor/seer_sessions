"""
Reflect, Mirror, and Move

1. **Top Reflection**:
    *   Take the value in the second column of the second row of the input grid (value 6) and put in 1st column of the 1st row of the output grid.
    *   Take the value in the first column of the third row of the input grid (value 2) and place two copies of it in the last two cells of the top row, to the right

2. **Middle Reflection**: The original 2x2 colored block remains in its original location in the output grid.

3. **Bottom Replication and mirroring**: Copy the top row of the 2x2 colored block and mirror it, such that [4,6] becomes [6,4]. Place this mirrored two-color block in the output grid starting two rows below the original block's lower edge. Copy the block again into the next row.
"""

import numpy as np

def get_2x2_block(grid):
    # Find the top-left corner of the 2x2 block of non-zero pixels.
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] != 0 and grid[i+1, j] != 0 and
                grid[i, j+1] != 0 and grid[i+1, j+1] != 0):
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid with zeros, same size as input.
    output_grid = np.zeros_like(input_grid)

    # Middle Reflection: Copy the 2x2 block to the same location in the output grid.
    block_start = get_2x2_block(input_grid)
    if block_start:
        i, j = block_start
        output_grid[i:i+2, j:j+2] = input_grid[i:i+2, j:j+2]

        # Top Reflection
        output_grid[0, 0] = input_grid[i, j+1]  # Value 6
        output_grid[0, -2] = input_grid[i+1,j]
        output_grid[0, -1] = input_grid[i+1,j]
        

        # Bottom Replication and mirroring.
        mirrored_row = input_grid[i, j:j+2][::-1]  # Mirror the top row of the block.
        output_grid[i+3, j] = mirrored_row[0]
        output_grid[i+3, j+1] = mirrored_row[1]
        output_grid[i+4, j] = mirrored_row[0]
        output_grid[i+4, j+1] = mirrored_row[1]


    return output_grid