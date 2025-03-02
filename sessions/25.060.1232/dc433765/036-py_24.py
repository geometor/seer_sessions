"""
1.  **Find the Green Pixel:** Locate the first instance of a green pixel (value 3) within the input grid. If no green pixel is found, the output is identical to the input.
2.  **Check for Adjacent Zero Rows:** Once the green pixel is found, check for the presence of an all-zero row immediately *above* the green pixel. Also check for the presence of an all-zero row immediately *below* the green pixel.
3.  **Conditional Row Removal:**
    *   If an all-zero row is found *above* the green pixel, remove that row.
    *   Otherwise, if an all-zero row is found *below* the green pixel, remove that row.
    *    If neither condition is met, do not modify the grid.
4.  **Output:** Return the resulting grid.
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
        return input_grid  # No green pixel, return input as is

    row_above_green = green_pixel_coords[0] - 1
    row_below_green = green_pixel_coords[0] + 1

    # Check for adjacent zero rows and remove if necessary.
    if check_row_zeros(input_grid, row_above_green):
        output_grid = remove_row(input_grid, row_above_green)
    elif check_row_zeros(input_grid, row_below_green):
        output_grid = remove_row(input_grid, row_below_green)
    else:
        output_grid = input_grid.copy() # No adjacent zero row, return a copy of input.

    return output_grid