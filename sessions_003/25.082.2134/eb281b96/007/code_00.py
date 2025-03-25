"""
The transformation rule involves replicating a given input pattern vertically to generate an output grid. The number of replications is determined by the ratio of the output height to the input height. The input pattern is repeated fully an integer number of times, with a potential partial replication at the end based on the fractional part of the height ratio. The width of the output is the same as the input.
"""

import numpy as np

def _replicate_pattern(input_grid, output_grid, height_ratio):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    full_replications = int(height_ratio)
    partial_replication_rows = int(round((height_ratio - full_replications) * input_height))

    for out_row in range(output_height):
        for out_col in range(output_width):
            if out_row < full_replications * input_height:
                in_row = out_row % input_height
            else:
                in_row = out_row - full_replications * input_height
            in_col = out_col  # Widths are the same
            output_grid[out_row, out_col] = input_grid[in_row, in_col]
    return output_grid

def transform(input_grid, output_grid): # added expected output to signature
    """
    Transforms the input grid by replicating its pattern vertically.
    The output's height is determined by the expected output. The replication
    factor is calculated as output_height / input_height.  Full and partial
    replications are performed based on this factor.
    """
    input_grid = np.array(input_grid)
    output_grid_expected = np.array(output_grid)  # Use expected output to define dimensions
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid_expected.shape

    # Calculate the height ratio
    height_ratio = output_height / input_height

    # Initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate the pattern
    output_grid = _replicate_pattern(input_grid, output_grid, height_ratio)

    return output_grid