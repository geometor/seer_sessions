"""
The input grid's border color and *one* of its inner colors are swapped with each other *and* the positions of the input's other inner color.
"""

import numpy as np

def get_border_color(grid):
    """Gets the border color of the grid (top-left pixel)."""
    return grid[0, 0]

def get_inner_colors(grid):
    """Gets the unique inner colors of the grid."""
    grid = np.array(grid)
    border_color = get_border_color(grid)
    inner_colors = np.unique(grid[1:-1, 1:-1])
    inner_colors = inner_colors[inner_colors != border_color]
    return inner_colors

def transform(input_grid):
    """Transforms the input grid by swapping colors as per the rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Get the border color of the input grid.
    input_border_color = get_border_color(input_grid)

    # Find the inner colors
    inner_colors = get_inner_colors(input_grid)
    
    if len(inner_colors) == 0:
      return output_grid.tolist()

    if len(inner_colors) == 1:
        output_border_color = inner_colors[0]
        output_grid[input_grid == input_border_color] = output_border_color
        output_grid[input_grid == output_border_color] = input_border_color
        return output_grid.tolist()
    
    # Determine which inner color swaps with the border.  Based on the examples,
    # it appears to be the *last* inner color in the sorted unique list.  This is a hypothesis
    # and needs further validation.

    output_border_color = inner_colors[-1]
    other_inner_color = inner_colors[0]


    # Swap the colors
    output_grid[input_grid == input_border_color] = output_border_color
    output_grid[input_grid == other_inner_color] = input_border_color
    output_grid[input_grid == output_border_color] = other_inner_color # this last one is needed!

    
    return output_grid.tolist()