"""
The input grid is transformed into a larger output grid by scaling up each pixel to a 2x2 block.
The scaled blocks are then arranged in the output grid based on a combination of horizontal and vertical reflections,
effectively mirroring the scaled quadrants of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into the output grid by scaling each pixel to a 2x2 block and arranging
    these blocks based on horizontal and vertical reflections.
    """
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Iterate through each cell of the input grid
    for i in range(input_height):
        for j in range(input_width):
            # Scale each pixel to a 2x2 block
            scaled_block = [
                [input_grid[i][j], input_grid[i][j]],
                [input_grid[i][j], input_grid[i][j]]
            ]

            # Determine the quadrant of the input pixel (conceptual quadrants)
            # Top-left quadrant: No reflection
            output_grid[2*i][2*j] = scaled_block[0][0]
            output_grid[2*i+1][2*j] = scaled_block[1][0]
            output_grid[2*i][2*j+1] = scaled_block[0][1]
            output_grid[2*i+1][2*j+1] = scaled_block[1][1]

            # Top-right quadrant: Horizontal reflection
            if 2*j+2 < output_width:
                output_grid[2*i][2*j+2] = scaled_block[0][1]
                output_grid[2*i+1][2*j+2] = scaled_block[1][1]
            if 2*j+3 < output_width:
                output_grid[2 * i][2 * j + 3] = scaled_block[0][0]
                output_grid[2 * i + 1][2 * j + 3] = scaled_block[1][0];

            # Bottom-left quadrant:  Vertical reflection
            if 2*i+2 < output_height:
                output_grid[2*i+2][2*j] = scaled_block[1][0]
                output_grid[2*i+2][2*j+1] = scaled_block[1][1]

            if 2*i+3 < output_height:
                output_grid[2 * i + 3][2 * j] = scaled_block[0][0]
                output_grid[2 * i + 3][2 * j + 1] = scaled_block[0][1]

            #bottom-right quadrant: horizontal and vertical
            if 2*i+2 < output_height and 2*j+2 < output_width:
                output_grid[2*i+2][2*j+2] = scaled_block[1][1]
            if 2*i+2 < output_height and 2*j+3 < output_width:
                output_grid[2*i+2][2*j+3] = scaled_block[1][0]
            if 2*i+3 < output_height and 2*j+2 < output_width:
                output_grid[2*i+3][2*j+2] = scaled_block[0][1]
            if 2*i+3 < output_height and 2*j+3 < output_width:
                output_grid[2*i+3][2*j+3] = scaled_block[0][0]


    return output_grid