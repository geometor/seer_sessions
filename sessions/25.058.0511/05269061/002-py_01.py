"""
The transformation rule identifies a 3x3 pattern in the top-left corner of the input grid and extends it both vertically and horizontally to fill the entire output grid. The extension maintains the relative positions of the colors within the pattern and alternates them in the rows and columms.
"""

import numpy as np

def get_top_left_pattern(grid):
    """Extracts the 3x3 top-left pattern from the input grid."""
    return grid[:3, :3]

def extend_pattern(input_grid):
    """Extends the 3x3 top-left pattern to fill the output grid."""
    pattern = get_top_left_pattern(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # build first three columns
    for i in range(3):
        for j in range(rows):
            output_grid[j,i] = pattern[j % 3, i]

    # extend the pattern horizontally
    for i in range(3):
        for j in range(3,cols):
            output_grid[:,j] = np.roll(output_grid[:,j-3],1)  # shift the colors to the right

    return output_grid

def transform(input_grid):
    """Transforms the input grid by extending the top-left 3x3 pattern."""
    # Initialize the output grid with the same dimensions as the input.
    output_grid = extend_pattern(input_grid)


    return output_grid