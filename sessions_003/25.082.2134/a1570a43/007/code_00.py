"""
The transformation rule involves repositioning contiguous blocks of red (2) pixels to the rightmost possible position within their respective rows. The movement is constrained by green (3) pixels, other non-contiguous red pixels, and the grid's right edge.  Empty (0) pixels between blocks should be preserved.  The shift is cumulative, meaning all red blocks in a row are shifted together, maintaining their relative spacing.
"""

import numpy as np

def _find_red_blocks(row):
    """
    Identifies contiguous blocks of red pixels in a row.
    Returns a list of tuples, where each tuple represents a block
    as (start_index, end_index).
    """
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == 2:
            if not in_block:
                in_block = True
                start_index = i
        elif in_block:
            in_block = False
            blocks.append((start_index, i - 1))
    if in_block:
        blocks.append((start_index, len(row) - 1))
    return blocks

def _calculate_cumulative_shift(row, red_blocks):
    """
    Calculates the total available shift for red blocks in a row.
    """
    if not red_blocks:
        return 0

    last_red_index = red_blocks[-1][1]
    shift = 0
    for i in range(last_red_index + 1, len(row)):
        if row[i] == 0:
            shift += 1
        else:
            break # Stop at the first non-empty pixel
    return shift
def _shift_blocks(row, red_blocks, shift):
    """
        shift the blocks to preserve the spacing between them
    """
    new_row = np.copy(row)

    # clear all red cells
    for start, end in red_blocks:
        new_row[start:end+1] = 0

    # move all blocks using cumulative shift
    for start, end in reversed(red_blocks):
        length = end - start + 1
        new_end = end + shift
        
        #check for blocking
        for i in range(end+1, new_end+1):
            if i >= len(row) or row[i] != 0:
                new_end = i-1
                break
                
        new_start = new_end - length + 1

        #check for valid move before assignment
        if new_start >= 0:
          new_row[new_start:new_end + 1] = 2
        
    return new_row

def transform(input_grid):
    """
    Transforms the input grid by moving blocks of red pixels to the right,
    constrained by green pixels, other red pixels, and the grid edge,
    preserving spaces.  The shift is cumulative for all red blocks in a row.
    """
    output_grid = np.copy(input_grid)
    rows, _ = output_grid.shape

    # Iterate through each row
    for r in range(rows):
        row = output_grid[r]
        # Find red blocks in the current row
        red_blocks = _find_red_blocks(row)

        # Calculate the cumulative shift for all blocks
        shift = _calculate_cumulative_shift(row, red_blocks)
        
        # shift with spacing
        output_grid[r] = _shift_blocks(row, red_blocks, shift)

    return output_grid