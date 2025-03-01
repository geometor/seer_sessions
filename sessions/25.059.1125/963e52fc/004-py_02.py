"""
The transformation rule is to double the width of the input grid. The central colored rows (alternating red and azure) are replicated horizontally, while the white rows are extended to the new width.
"""

import numpy as np

def get_colored_rows(grid):
    # helper to find rows with non-zero values
    colored_rows = []
    for i, row in enumerate(grid):
        if np.any(row != 0):
            colored_rows.append(i)
    return colored_rows

def transform(input_grid):
    """
    Transforms the input grid by doubling its width. Colored rows are replicated, and white rows are extended.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Find the rows with colors (non-zero values)
    colored_rows_indices = get_colored_rows(input_grid)

    # Iterate through each row of input and perform transformations
    for i in range(rows):
      if i in colored_rows_indices:
        # replicate colored row by concatenating it with itself
        output_grid[i,:] = np.concatenate((input_grid[i,:], input_grid[i,:]))
      else:
        # extend white row
        output_grid[i,:] = np.concatenate((input_grid[i,:], input_grid[i,:]))

    return output_grid.tolist()