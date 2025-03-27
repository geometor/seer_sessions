"""
Transforms the input grid by representing each row's non-background blocks.
Empty rows (all 1s) are represented as [0]. Non-empty rows are represented
by the color of each contiguous block of non-1 pixels, repeated for the
number of pixels in that block within the row. Output rows are padded with 0s
to match the width of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    input_grid = np.array(input_grid)
    output_grid = []
    num_cols = input_grid.shape[1]

    for row in input_grid:
        # Handle empty rows (all 1s)
        if np.all(row == 1):
            output_row = [0] * num_cols  # Pad with 0s to match input width
            output_grid.append(output_row)
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

        # Pad the output row with 0s to match input width
        padding_needed = num_cols - len(row_output)
        row_output.extend([0] * padding_needed)

        output_grid.append(row_output)

    return output_grid