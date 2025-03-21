"""
Divides the input grid into six blocks based on its dimensions. Then, it checks each block: if any element within the block
is non-zero, the corresponding element in the output grid is set to 3; otherwise, it's set to 0.
"""

import numpy as np

def get_blocks(input_grid):
    blocks = []
    
    #first block
    blocks.append(input_grid[0:3, 0:1])

    #second block
    blocks.append(input_grid[0:3, 1:2])
    
    #third block
    blocks.append(input_grid[0:3, 2:3])

    #fourth block
    blocks.append(input_grid[0:3, 3:4])

    #fifth block
    blocks.append(input_grid[3:4, 0:4])

    #sixth block
    blocks.append(input_grid[4:9, 0:4])
    
    return blocks

def check_block_for_non_zero(block):
    # Check if any element in the block is non-zero.
    return np.any(block != 0)


def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Get blocks from the input grid
    blocks = get_blocks(np.array(input_grid))

    # Map input blocks to output grid cells
    block_mapping = {
        0: (0, 0),  # top-left
        1: (0, 1),
        2: (0, 2),
        3: (0, 3),
        4: (1, 0), # center
        5: (2, 0),
    }

    row_offset = 0
    col_offset = 0

    #change output pixels
    for i in range(len(blocks)):
        if i<4:
           row_offset = 0
           col_offset = i
        if i==4:
            row_offset = 1
            col_offset = 0
        elif i==5:
            row_offset = 2
            col_offset = 0
        if check_block_for_non_zero(blocks[i]):
            output_grid[row_offset, col_offset] = 3
        else:
            output_grid[row_offset,col_offset] = 0

    output_grid[3,0] = output_grid[2,0]
    output_grid[3,1] = output_grid[0,0]
    output_grid[3,2] = output_grid[0,3]
    output_grid[2,0] = output_grid[1,0]


    return output_grid