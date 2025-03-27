"""
The transformation rule takes the input grid, repeats it four times horizontally while preserving the row order and color positions to achieve the consistent output grid width of 12 and height equal to input height.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height, 12), dtype=int)

    # Horizontal Repetition: The input grid is repeated four times horizontally.
    for i in range(4):
        output_grid[:, i * input_width : (i + 1) * input_width] = input_grid

    return output_grid.tolist()