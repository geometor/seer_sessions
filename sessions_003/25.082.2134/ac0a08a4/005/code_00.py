"""
Transforms the input grid into an output grid by expanding each non-zero pixel into a block. The size of each block is dynamically determined by zero-valued pixels or grid boundaries.
"""

import numpy as np

def expand_pixel(input_grid, output_grid, row, col, pixel_value):
    """Expands a single pixel to its maximum bounds."""
    output_height, output_width = output_grid.shape
    input_height, input_width = input_grid.shape

    # Find expansion boundaries
    top = row
    while top > 0 and input_grid[top - 1, col] == 0:
        top -= 1
    bottom = row
    while bottom < input_height - 1 and input_grid[bottom + 1, col] == 0:
        bottom += 1
    left = col
    while left > 0 and input_grid[row, left - 1] == 0:
        left -= 1
    right = col
    while right < input_width - 1 and input_grid[row, right + 1] == 0:
        right += 1
    
    # get scaling factor
    vertical_scale = output_height//input_height
    horizontal_scale = output_width//input_width
    
    # Adjust boundaries to the output grid
    top *= vertical_scale
    bottom *= vertical_scale
    left *= horizontal_scale
    right *= horizontal_scale
        
    # print(f'input[{row},{col}] = {pixel_value}')
    # print(f'{top=}')
    # print(f'{bottom=}')
    # print(f'{left=}')
    # print(f'{right=}')

    # Fill the corresponding block in the output grid
    for i in range(top, min(top + vertical_scale, output_height)):
        for j in range(left, min(left + horizontal_scale, output_width)):
            # print(f'setting {i=},{j=}={pixel_value}')
            output_grid[i, j] = pixel_value


def transform(input_grid, output_grid):

    # Iterate through each pixel of the input grid
    for row_index in range(input_grid.shape[0]):
        for col_index in range(input_grid.shape[1]):
            pixel_value = input_grid[row_index, col_index]

            # If the pixel is non-zero, expand it
            if pixel_value != 0:
                expand_pixel(input_grid, output_grid, row_index, col_index, pixel_value)

    return output_grid