"""
The transformation rule is a 2x2 replication of the input grid. The output grid's dimensions are double the input grid's dimensions in both height and width.  The input grid is copied directly to the top-left quadrant of the output grid. The top-right, bottom-left, and bottom-right quadrants are also direct copies of the original input grid. It is *not* a mirroring operation, but a direct replication in all four quadrants formed by doubling the input.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by replicating it in a 2x2 grid."""

    input_height, input_width = input_grid.shape

    # Calculate output dimensions.
    output_height = input_height * 2
    output_width = input_width * 2

    # Create output grid initialized with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy input grid to top-left quadrant.
    output_grid[:input_height, :input_width] = input_grid

    # Copy to top-right quadrant.
    output_grid[:input_height, input_width:] = input_grid

    # Copy to bottom-left quadrant
    output_grid[input_height:, :input_width] = input_grid
    
    # Copy to bottom-right quadrant.
    output_grid[input_height:, input_width:] = input_grid

    return output_grid