"""
The transformation extracts rectangular subgrids of colors different from the background color and places them in a standardized 3x3 output grid. The subgrids are placed based on their vertical order of appearance in the input grid. The first appearing subgrid's color goes in the top row (row 0, middle column), and the second in the bottom row (row 2, middle column). If a subgrid color doesn't exist, the corresponding output cell is black (0). The output size is always 3x3.
"""

import numpy as np

def get_subgrids(grid):
    """Extracts rectangular subgrids of colors different from the background."""
    background_color = grid[0, 0]
    unique_colors = np.unique(grid)
    foreground_colors = [color for color in unique_colors if color != background_color]

    subgrids = {}
    for color in foreground_colors:
        rows, cols = np.where(grid == color)
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        subgrid = grid[min_row:max_row+1, min_col:max_col+1]
        subgrids[color] = subgrid
    return subgrids

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize a 3x3 output grid filled with black (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Get subgrids
    subgrids = get_subgrids(input_grid)

    # Sort subgrids by their vertical order of appearance (top to bottom)
    sorted_colors = sorted(subgrids.keys(), key=lambda color: np.min(np.where(input_grid == color)[0]))
  
    # Place the subgrid colors in the output grid based on vertical order
    if len(sorted_colors) >= 1:
        output_grid[0, 1] = sorted_colors[0] # First subgrid color
    if len(sorted_colors) >= 2:
        output_grid[2, 1] = sorted_colors[1]  # Second subgrid color

    return output_grid