"""
The transformation removes either a solid-color row along the bottom edge of the grid, or a dominant "background" color.
"""

import numpy as np

def get_bottom_row(grid):
    """Returns the bottom row of the grid."""
    return grid[-1, :]

def is_solid_color(row):
    """Checks if a row is of a single color."""
    return np.all(row == row[0])

def get_dominant_color(grid):
    """find color that takes the majority of the grid."""
    counts = np.bincount(grid.flatten())
    return np.argmax(counts)

def remove_row(grid, row_index):
    """Removes a row from the grid."""
    return np.delete(grid, row_index, axis=0)

def remove_color(grid, color):
    """ remove specific color from grid"""
    rows, cols = grid.shape
    new_grid = []

    for r in range(rows):
      new_row = []
      for c in range(cols):
        if grid[r][c]!=color:
          new_row.append(grid[r][c])
      if len(new_row) > 0:
        new_grid.append(new_row)

    return np.array(new_grid)

def transform(input_grid):
    """
    Removes either the solid-color bottom row or a dominant color from the input grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid)

    # Check if the bottom row is solid color
    bottom_row = get_bottom_row(grid)
    if is_solid_color(bottom_row):
        # Remove the bottom row
        output_grid = remove_row(grid, grid.shape[0] - 1)
        return output_grid.tolist()
    else:
        dominant_color = get_dominant_color(grid)
        output_grid = remove_color(grid, dominant_color)
        return output_grid.tolist()


