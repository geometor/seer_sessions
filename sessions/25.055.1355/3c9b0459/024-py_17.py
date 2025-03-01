"""
In each input grid, identify the columns with a uniform color.  Find the column that matches a specific color (this color varies across examples, but appears to always be the color in the second column, index 1). Move this identified column to the leftmost position (index 0) of the output grid. The remaining columns maintain their relative order.
"""

import numpy as np

def get_uniform_columns(grid):
    # Find columns in the grid that have a uniform color.
    uniform_columns = []
    for i in range(grid.shape[1]):
        if len(set(grid[:, i])) == 1:
            uniform_columns.append((i, grid[0, i]))  # (index, color)
    return uniform_columns

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Get uniform columns
    uniform_cols = get_uniform_columns(input_grid)

    # Find the color of the second column (if it exists and is uniform)
    target_color = None
    for index, color in uniform_cols:
        if index == 1:
            target_color = color
            break

    if target_color is None:
        return output_grid # return original if no target

    # Find the index of the column with the target color
    target_index = None
    for index, color in uniform_cols:
        if color == target_color:
            target_index = index
            break

    if target_index is None: # should never occur, since target came from the list, but safe
        return output_grid

    # Move the target column to the leftmost position
    target_column = input_grid[:, target_index].copy()
    output_grid[:, 0] = target_column

    # Shift other columns to the right, maintaining relative order
    col_idx = 1
    for i in range(input_grid.shape[1]):
        if i != target_index:
            output_grid[:, col_idx] = input_grid[:, i].copy()
            col_idx += 1

    return output_grid