"""
The transformation rule is as follows: Find the green pixel (value 3) in the input grid.
Check if the row directly above the green pixel has all values equal to zero.
If the identified row consists only of zeros, create a new grid by removing this row from the input grid.
Otherwise, copy the entire input grid without changes. Return the resulting grid.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return row, col
    return None

def check_row_zeros(grid, row_index):
    """Checks if all elements in a specified row are zero."""
    if row_index < 0 or row_index >= grid.shape[0]:
        return False  # Row index out of bounds
    return np.all(grid[row_index] == 0)

def remove_row(grid, row_index):
    """Removes a row from the grid."""
    return np.delete(grid, row_index, axis=0)

def transform(input_grid):
    # Find the green pixel (value 3).
    green_pixel_coords = find_pixel(input_grid, 3)
    
    if green_pixel_coords is None:
      return input_grid
    
    row_above_green = green_pixel_coords[0] - 1

    # Check if the row above the green pixel has all zeros.
    if check_row_zeros(input_grid, row_above_green):
        # Remove the all-zero row.
        output_grid = remove_row(input_grid, row_above_green)
    else:
        # Copy the input grid as is.
        output_grid = input_grid.copy()

    return output_grid