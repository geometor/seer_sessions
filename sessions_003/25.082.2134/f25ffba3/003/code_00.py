"""
The input grid is divided into two equal sections: the top half (rows 0-4) and the bottom half (rows 5-9). The top half of the input grid is vertically flipped (rows are reversed) and becomes the top half of the output grid. The bottom half of the input grid is copied directly to the bottom half of the output grid without any changes.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Divide the grid into top and bottom halves.
    mid_row = rows // 2

    # Vertically flip the top half.
    top_half = input_grid[:mid_row, :]
    flipped_top_half = np.flip(top_half, axis=0)
    output_grid[:mid_row, :] = flipped_top_half

    # Copy the bottom half directly.
    bottom_half = input_grid[mid_row:, :]
    output_grid[mid_row:, :] = bottom_half

    return output_grid