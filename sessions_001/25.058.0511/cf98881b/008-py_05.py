"""
The transformation extracts columns from the input grid that start with colors 4 (yellow), 0 (white), 1 (blue), or 9 (maroon) and places them into a new grid.
"""

import numpy as np

def get_columns_starting_with_colors(grid, colors):
    """
    Identifies and returns columns that start with specified colors.
    """
    selected_columns = []
    for j in range(grid.shape[1]):
        if grid[0, j] in colors:
            selected_columns.append(grid[:, j])
    return selected_columns

def transform(input_grid):
    """
    Transforms the input grid by selecting columns starting with specified colors
    and arranging them into a new output grid.
    """
    # Define the target colors
    target_colors = [4, 0, 1, 9]

    # Get columns starting with the target colors
    selected_columns = get_columns_starting_with_colors(input_grid, target_colors)

    # Initialize the output grid
    output_grid = np.zeros((input_grid.shape[0], len(selected_columns)), dtype=int)

    # Fill in output
    for i, col in enumerate(selected_columns):
        output_grid[:,i] = col

    return output_grid