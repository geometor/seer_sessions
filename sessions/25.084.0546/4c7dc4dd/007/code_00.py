"""
Transforms an input grid by extracting a subgrid based on the top-left pixel's
color, filtering the subgrid's colors, and applying a special rule if
applicable.

1. Subgrid Extraction:
    - If the top-left pixel is blue (1), extract a 5x5 subgrid.
    - If the top-left pixel is yellow (4), extract a 4x4 subgrid.
    - If the top-left is not blue or yellow, return an empty grid.

2. Color Filtering:
    - Change all non-red (2) pixels in the subgrid to black (0).

3. Special Rule (5x5 subgrids only):
    - If the extracted subgrid is 5x5, check if the first row of the output
      grid is all black (0).
    - If it is, change the first row to magenta (6).
"""

import numpy as np

def get_subgrid(input_grid, size):
    """Extracts a subgrid of the given size from the top-left corner."""
    return input_grid[:size, :size]

def filter_colors(grid):
    """Changes all non-red (2) pixels in the grid to black (0)."""
    filtered_grid = grid.copy()
    filtered_grid[filtered_grid != 2] = 0
    return filtered_grid

def apply_special_rule(grid):
    """Changes the first row to magenta (6) if it's all black (0)."""
    modified_grid = grid.copy()
    if modified_grid.shape[0] > 0 and np.all(modified_grid[0, :] == 0):
        modified_grid[0, :] = 6
    return modified_grid

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    top_left_color = input_grid[0, 0]
    output_grid = None

    if top_left_color == 1:  # Blue
        subgrid = get_subgrid(input_grid, 5)
        filtered_subgrid = filter_colors(subgrid)
        output_grid = apply_special_rule(filtered_subgrid)
    elif top_left_color == 4:  # Yellow
        subgrid = get_subgrid(input_grid, 4)
        output_grid = filter_colors(subgrid)
    else: # Handle cases where top-left is not blue or yellow
       output_grid = np.zeros((0,0), dtype=int)

    return output_grid