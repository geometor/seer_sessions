"""
1.  **Identify Objects:** Identify all contiguous regions of magenta (color 6) pixels and gray (color 5) pixels. The white (0) pixels represent the background.
2.  **Remove Gray:** Remove all gray objects from the grid.
3.  **Rotate Magenta:** Rotate the magenta object 90 degrees counter-clockwise. The pivot point for this rotation is a point within the magenta shape.
4.  **Remove Intersection:** After the rotation, remove the magenta pixel(s) that occupy the same position as a magenta pixel from the original unrotated figure. If there are no intersecting pixels, the magenta figure is unchanged.
5.  **Output:** The final grid contains only the rotated magenta object (with intersection removed) on the white background.
"""

import numpy as np

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def rotate_point(point, center):
    """Rotates a point 90 degrees counter-clockwise around a center."""
    row, col = point
    center_row, center_col = center
    translated_row = row - center_row
    translated_col = col - center_col
    rotated_row = -translated_col
    rotated_col = translated_row
    new_row = rotated_row + center_row
    new_col = rotated_col + center_col
    return (new_row, new_col)

def get_rotation_center(coords):
    """Calculates the center of rotation for a set of coordinates."""
    if len(coords) == 0:
       return None
    min_row = min(coords, key=lambda item: item[0])[0]
    max_row = max(coords, key=lambda item: item[0])[0]
    min_col = min(coords, key=lambda item: item[1])[1]
    max_col = max(coords, key=lambda item: item[1])[1]
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    return (center_row, center_col)

def rotate_magenta_object(grid, magenta_coords):
    """Rotates the magenta object 90 degrees counter-clockwise."""
    rotated_grid = np.copy(grid)
    center = get_rotation_center(magenta_coords)
    if center is None:
        return rotated_grid, []  # No magenta object to rotate

    new_magenta_coords = []
    for r, c in magenta_coords:
        rotated_grid[r, c] = 0  # Clear the original magenta pixel

    for r, c in magenta_coords:
        new_r, new_c = rotate_point((r, c), center)
        new_magenta_coords.append((new_r, new_c))

    return rotated_grid, new_magenta_coords

def remove_intersection(grid, original_coords, rotated_coords):
    """Removes intersecting pixels after rotation."""

    #create sets of tuples for comparisons
    original_set = set(map(tuple, original_coords))
    rotated_set = set(rotated_coords)

    intersection = original_set.intersection(rotated_set)
    for r, c in intersection:
      if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
        grid[r, c] = 0  # Remove intersecting pixels


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find and Remove Gray (5)
    gray_coords = find_object(output_grid, 5)
    if gray_coords is not None:
        for r, c in gray_coords:
            output_grid[r, c] = 0

    # Find Magenta (6)
    magenta_coords = find_object(output_grid, 6)
    if magenta_coords is None:
        return output_grid #no magenta, return

    # Rotate Magenta Object
    rotated_grid, new_magenta_coords = rotate_magenta_object(output_grid, magenta_coords)
    output_grid = rotated_grid

    #set new magenta pixels - within bounds
    valid_new_magenta_coords = []
    for r,c in new_magenta_coords:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          output_grid[r,c] = 6
          valid_new_magenta_coords.append( (r,c) )

    # Remove Intersection
    remove_intersection(output_grid, magenta_coords, valid_new_magenta_coords)

    return output_grid