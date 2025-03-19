"""
The input grid is divided into a 2x2 grid of equal-sized rectangular blocks of different colors. The output grid represents these blocks, where each block is represented by a pair of numbers, one for each color.
The order is top-left, top-right, middle-left, middle-right, bottom-left, bottom-right.
"""

import numpy as np

def get_block_color(grid, row_start, row_end, col_start, col_end):
    """Extracts the color of a block from the grid."""
    # we are interested in a single solid color
    first_color = grid[row_start, col_start]
    return first_color

def transform(input_grid):
    """Transforms the input grid into a sequence of color values representing the 2x2 blocks."""
    # Determine the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Calculate block dimensions. Each block is 6x6 in this example.
    # the grid is divided into six blocks, arranged as 2 cols x 3 rows
    block_height = rows // 3
    block_width = cols // 2

    # Initialize an empty list to store the output.
    output = []

    # Iterate through the blocks and get color.
    
    # top-left block
    color1 = get_block_color(input_grid, 0, block_height, 0, block_width)
    output.append(color1)

    # top-right block
    color2 = get_block_color(input_grid, 0, block_height, block_width, 2 * block_width)
    output.append(color2)
    
    # middle-left block
    color3 = get_block_color(input_grid, block_height, 2* block_height, 0, block_width)
    output.append(color3)

    # middle-right block
    color4 = get_block_color(input_grid, block_height, 2*block_height, block_width, 2 * block_width)
    output.append(color4)

    # bottom-left block
    color5 = get_block_color(input_grid, 2 * block_height, 3 * block_height, 0, block_width)
    output.append(color5)

    # bottom-right block
    color6 = get_block_color(input_grid, 2 * block_height, 3 * block_height, block_width, 2 * block_width)
    output.append(color6)
    
    output_grid = np.array(output).reshape(3,2)

    return output_grid