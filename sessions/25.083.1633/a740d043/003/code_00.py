"""
Transforms the input grid by representing each row's non-background blocks.
Empty rows (all 1s) are represented as [0]. Non-empty rows are represented
by the color of each contiguous block of non-1 pixels, repeated for the
number of pixels in that block within the row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    input_grid = np.array(input_grid)
    output_grid = []

    for row in input_grid:
        # Handle empty rows (all 1s)
        if np.all(row == 1):
            output_grid.append([0])
            continue

        # Find contiguous blocks of non-1 pixels in the row
        row_output = []
        current_block = []
        for pixel in row:
            if pixel != 1:
                current_block.append(pixel)
            else:
                if current_block:
                    row_output.extend([current_block[0]] * len(current_block))
                    current_block = []
        if current_block:  # Handle any remaining block at the end of the row
            row_output.extend([current_block[0]] * len(current_block))

        if len(row_output) > 0: #add to output
            output_grid.append(row_output)
        else: #add [0] if all 1 and no output yet
            output_grid.append([0])


    return output_grid