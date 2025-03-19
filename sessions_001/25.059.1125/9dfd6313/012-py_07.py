"""
1.  **Identify the gray pixel (color 5) within the input grid.** This pixel is the center of rotation.
2.  **Identify pixels surrounding the center gray pixel.** It appears the
    pixels immediately surrounding the gray center will be rotated.
3.  **Rotate select pixels 90 degrees clockwise around the gray center pixel.**
    The row and column of each moving pixel, relative to the gray pixel are
    swapped and inverted to calculate new positions.
4.  **Create output grid** Copy all pixels from the input grid to the same
    position in the output grid.
5.  **Update the output grid**: Move the select pixels that were rotated to
    their new positions on the output grid.
"""

import numpy as np

def find_gray_center(grid):
    """Finds the coordinates of the gray pixel (color 5) in the grid."""
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 5:
                return (row_idx, col_idx)
    return None  # Should not happen in these tasks, but good practice

def get_surrounding_pixels(grid, center):
    """Gets the coordinates and values of pixels surrounding the center."""
    row, col = center
    surrounding = []
    for i in range(max(0, row - 1), min(grid.shape[0], row + 2)):
        for j in range(max(0, col - 1), min(grid.shape[1], col + 2)):
            if (i, j) != center:
                surrounding.append(((i, j), grid[i, j]))
    return surrounding

def rotate_point(point, center):
    """Rotates a point 90 degrees clockwise around a center point."""
    row, col = point
    center_row, center_col = center
    new_row = center_row + (col - center_col)
    new_col = center_col - (row - center_row)
    return (new_row, new_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the gray center pixel.
    center = find_gray_center(input_grid)

    # Get surrounding pixels.
    surrounding_pixels = get_surrounding_pixels(input_grid, center)

    # Rotate surrounding pixels and update the output grid.
    for (row, col), value in surrounding_pixels:
        rotated_coords = rotate_point((row, col), center)
        #check if rotated coordinates is within output_grid
        if 0 <= rotated_coords[0] < output_grid.shape[0] and 0 <= rotated_coords[1] < output_grid.shape[1]:
           output_grid[rotated_coords] = value
           #clear the original position if it will be rotated
           if (rotate_point(rotated_coords,center) != (row, col)):
              output_grid[row,col] = 0

    return output_grid