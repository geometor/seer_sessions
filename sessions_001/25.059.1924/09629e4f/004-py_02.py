"""
Transforms the input grid by creating blocks of solid color within regions defined by grey (5) horizontal lines.
"""

import numpy as np

def get_regions(grid):
    """
    Divides the grid into three regions based on grey (5) horizontal lines.
    Assumes there are always two such lines.
    """
    grey_rows = np.where((grid == 5).all(axis=1))[0]
    top_region = grid[:grey_rows[0], :]
    middle_region = grid[grey_rows[0] + 1:grey_rows[1], :]
    bottom_region = grid[grey_rows[1] + 1:, :]
    return top_region, middle_region, bottom_region, grey_rows

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get regions and divider row indices
    top_region, middle_region, bottom_region, grey_rows = get_regions(input_grid)

    # Transform Top Region
    output_grid[:grey_rows[0], :3] = 2  # 3x3 red block
    output_grid[:grey_rows[0], 3:7] = 0 #clear area

    # Transform Middle Region
    output_grid[grey_rows[0] + 1:grey_rows[1], :3] = 0
    # Keep 5 (central 3x3 block will be taken care of due to copy initialization)
    #keep 4
    #keep 3

    # Transform Bottom Region
    output_grid[grey_rows[1] + 1:, :3] = 6  # 3x3 magenta block
    output_grid[grey_rows[1] + 1:, 3:7] = 0

    return output_grid