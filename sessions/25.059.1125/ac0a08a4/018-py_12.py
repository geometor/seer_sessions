"""
Expands a 3x3 input grid into a 15x15 output grid. Non-zero pixels in the input
are expanded into 5x5 blocks of the same color in the output. Zero pixels are
handled differently depending on whether there are non-zero pixels in the same
row or column.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 15x15 output grid filled with zeros.
    output_grid = np.zeros((15, 15), dtype=int)

    # Iterate through each pixel of the 3x3 input grid.
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            pixel_value = input_grid[i, j]

            # Determine the top-left corner of the 5x5 block.
            row_start = i * 5
            col_start = j * 5

            if pixel_value != 0:
                # Fill the 5x5 block with the value of the input pixel.
                output_grid[row_start:row_start + 5, col_start:col_start + 5] = pixel_value
            else:
                # Zero Pixel Handling
                # Check for non-zero pixels in the same row or column
                non_zero_in_row = any(input_grid[i, k] != 0 for k in range(input_grid.shape[1]))
                non_zero_in_col = any(input_grid[k, j] != 0 for k in range(input_grid.shape[0]))

                if non_zero_in_row or non_zero_in_col:
                    # Find the non-zero value to propagate
                    if non_zero_in_row:
                        for k in range(input_grid.shape[1]):
                            if input_grid[i,k] != 0:
                                fill_value = input_grid[i,k]
                                break
                    elif non_zero_in_col:
                        for k in range(input_grid.shape[0]):
                            if input_grid[k,j] != 0:
                                fill_value = input_grid[k, j]
                                break

                    # output the block
                    output_grid[row_start:row_start+5, col_start:col_start+5] = fill_value
                # else:  # implicit from initialization with 0
                #     pass

    return output_grid