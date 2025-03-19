"""
The transformation rule is to double the width of the input grid. The central colored rows (alternating red and azure) are replicated by copying the colored block and appending it to the output. White rows are simply extended to the new width.
"""

import numpy as np

def get_colored_block(row):
    # helper to extract the start and end indices of the colored block in a row
    start = -1
    end = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start == -1:
                start = i
            end = i
    return start, end

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Iterate through each row
    for i, row in enumerate(input_grid):
        # check if it's a white row
        if np.all(row == 0):
            # extend white row
            output_grid[i, :] = np.concatenate((row, row))
        else:
            # Process colored rows
            start, end = get_colored_block(row)
            colored_block = row[start:end+1]

            # copy and append the colored block. Pad with white cells
            new_row = np.concatenate((row[0:end+1], colored_block))
            output_grid[i, :len(new_row)] = new_row


    return output_grid.tolist()