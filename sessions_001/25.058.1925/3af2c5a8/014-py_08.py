"""
1. **Expansion:** The output grid's dimensions are double the input grid's dimensions (both width and height).
2. **Replication:** Each pixel from the input grid is replicated as a 2x2 block of pixels with the same color in the output grid. So, `input[i][j]` becomes `output[2i][2j]`, `output[2i+1][2j]`, `output[2i][2j+1]`, and `output[2i+1][2j+1]`.
3. **Color Swapping:** In some cases, colors of the replicated pixels are swapped based on a one-to-one mapping between input and output colors. This mapping is consistent within a single task but may change between tasks. If a color does not have a mapping, it remains the same.
"""

import numpy as np

def get_color_swap_mapping(input_grid, output_grid):
    """
    Determines the color swapping rules between input and output grids.
    """
    color_map = {}
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    if output_height != 2 * input_height or output_width != 2 * input_width:
        return color_map  # Return empty map if dimensions don't follow 2x rule

    for i in range(input_height):
        for j in range(input_width):
            input_color = input_grid[i, j]
            output_color = output_grid[2*i, 2*j] # Check just one of the replicated pixels

            if input_color != output_color:
                if input_color not in color_map:
                    color_map[input_color] = output_color
                elif color_map[input_color] != output_color:
                    # Inconsistency detected
                    return {}  # Clear and return empty mapping

    return color_map
                    

def transform(input_grid, color_map=None):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # replicate and insert rows and columns
    for i in range(input_height):
        for j in range(input_width):
            input_color = input_grid[i, j]
            # Apply color swapping if a mapping is provided
            output_color = color_map.get(input_color, input_color) if color_map else input_color
            
            output_grid[2*i, 2*j] = output_color
            output_grid[2*i+1, 2*j] = output_color
            output_grid[2*i, 2*j+1] = output_color
            output_grid[2*i+1, 2*j+1] = output_color

    return output_grid