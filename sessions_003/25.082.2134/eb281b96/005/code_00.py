"""
The transformation rule involves replicating a given input pattern to generate an output grid. The input pattern is repeated vertically a certain number of times, potentially with a partial repetition at the end. The width of the output is the same as the input.
"""

import numpy as np

def _replicate_pattern(input_grid, output_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    for out_row in range(output_height):
        for out_col in range(output_width):
            in_row = out_row % input_height
            in_col = out_col % input_width # not needed because width matches
            output_grid[out_row, out_col] = input_grid[in_row, in_col]

    return output_grid

def transform(input_grid, output_grid): # added expected output to signature
    """
    Transforms the input grid by replicating its pattern vertically.
    The output's height is determined by the expected output, and
    the width is the same as the input's width.
    """
    input_grid = np.array(input_grid)
    output_grid_expected = np.array(output_grid) # rename to avoid confusion
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid_expected.shape

    # Initialize the output grid with zeros and correct dimensions
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Replicate the pattern
    output_grid = _replicate_pattern(input_grid, output_grid)
    
    return output_grid