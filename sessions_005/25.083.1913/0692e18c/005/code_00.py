"""
The output grid is a 9x9 grid. The input grid, along with its horizontally flipped, vertically flipped, and both horizontally and vertically flipped versions, are placed within the output grid. The original input is placed at the top-left corner. The horizontally flipped version is placed at the top-right corner. The vertically flipped version is placed at the bottom-left corner. The version flipped both horizontally and vertically is placed in the center of the output grid. The placements cause overlapping of pixels.
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

    # Top-Left Placement (Original)
    output_grid[:input_rows, :input_cols] = input_grid

    # Top-Right Placement (Horizontal Flip)
    output_grid[:input_rows, 9 - input_cols:] = flip_horizontal(input_grid)

    # Bottom-Left Placement (Vertical Flip)
    output_grid[9 - input_rows:, :input_cols] = flip_vertical(input_grid)
    
    # Center Placement (Horizontal and Vertical Flip)
    center_row_start = (9 - input_rows) // 2
    center_col_start = (9 - input_cols) // 2
    output_grid[center_row_start:center_row_start + input_rows, center_col_start:center_col_start + input_cols] = flip_vertical(flip_horizontal(input_grid))


    return output_grid.tolist()