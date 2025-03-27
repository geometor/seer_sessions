"""
The input grid is replicated and repositioned within a larger 9x9 output grid. The original input is placed at top-left. A horizontally mirrored copy is placed at top-right, and a vertically mirrored one goes to the bottom-left. A completely mirrored version (both horizontal and vertical) is placed at the center of the output grid.
"""

import numpy as np

def flip_horizontal(grid):
    return np.fliplr(grid)

def flip_vertical(grid):
    return np.flipud(grid)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)
    input_grid = np.array(input_grid)
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    # Top-Left Placement
    output_grid[:input_rows, :input_cols] = input_grid

    # Top-Right Placement: flip horizontally
    h_offset = output_cols - input_cols
    output_grid[:input_rows, h_offset:] = flip_horizontal(input_grid)

    # Bottom-Left Placement: flip vertically
    v_offset = output_rows - input_rows
    output_grid[v_offset:, :input_cols] = flip_vertical(input_grid)

    # Center Placement: flip both horiz and vert
    center_row_offset = (output_rows - input_rows) // 2
    center_col_offset = (output_cols - input_cols) // 2
    output_grid[center_row_offset:center_row_offset + input_rows, center_col_offset:center_col_offset + input_cols] = flip_vertical(flip_horizontal(input_grid))

    return output_grid.tolist()