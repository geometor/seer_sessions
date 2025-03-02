"""
1.  **Identify Objects:** Identify contiguous regions of magenta (6) and gray (5) pixels. White (0) is the background.
2.  **Remove Gray:** Remove all gray objects from the grid.
3.  **Rotate Magenta:** Rotate the magenta object 90 degrees counter-clockwise. The center of rotation is the magenta pixel in the input grid which, after rotation, would be the lowest of the topmost magenta pixels of the output grid.
4.  **Adjust After Rotation:** After rotating, shift the entire magenta object down by one row, *if* after the rotation, the bottom edge of the magenta object is on the same row as the bottom edge of the *unrotated* magenta object.  If not, leave as rotated.
5.  **Output:** The final grid contains only the rotated and potentially adjusted magenta object on the white background.
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

def get_rotation_center(magenta_coords, output_coords):
    """
    Calculates the center of rotation. The center is defined as the magenta
    pixel that, after a 90 degree counter clockwise rotation, ends at the
    lowest of the top-most pixels of the output
    """

    #find top row of the output
    min_row_out = min(output_coords, key=lambda item: item[0])[0]
    top_output_coords = [ (r,c) for r,c in output_coords if r == min_row_out ]
    #of the top row, find lowest (right-most)
    lowest_top = max(top_output_coords, key=lambda item: item[1])

    #find matching pixel in input
    for r, c in magenta_coords:
      rotated_r, rotated_c = rotate_point( (r,c), (r,c) )
      if (rotated_r, rotated_c) == lowest_top:
        return (r,c)

    return None


def rotate_magenta_object(grid, magenta_coords, center):
    """Rotates the magenta object 90 degrees counter-clockwise."""
    rotated_grid = np.copy(grid)
    if center is None:
        return rotated_grid, []  # No magenta object to rotate

    new_magenta_coords = []
    for r, c in magenta_coords:
        rotated_grid[r, c] = 0  # Clear the original magenta pixel

    for r, c in magenta_coords:
        new_r, new_c = rotate_point((r, c), center)
        new_magenta_coords.append((new_r, new_c))

    return rotated_grid, new_magenta_coords

def adjust_after_rotation(grid, original_coords, rotated_coords):
    """
    Shifts the rotated object down by one row if the bottom edge of the
    rotated object is on the same row as the bottom edge of the original
    object.
    """
    if not original_coords or not rotated_coords:
        return grid

    original_bottom_row = max(original_coords, key=lambda item: item[0])[0]
    rotated_bottom_row = max(rotated_coords, key=lambda item: item[0])[0]

    if original_bottom_row == rotated_bottom_row:
        shifted_coords = [(r + 1, c) for r, c in rotated_coords]
        #clear existing
        for r, c in rotated_coords:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                grid[r,c] = 0

        #add shifted
        for r, c in shifted_coords:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                grid[r, c] = 6


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

    #predict output coords
    rotated_grid, predicted_coords = rotate_magenta_object(output_grid, magenta_coords, magenta_coords[0])
    valid_predicted_coords = []
    for r,c in predicted_coords:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          rotated_grid[r,c] = 6 #temp set to find center
          valid_predicted_coords.append( (r,c) )

    # Rotate Magenta Object
    center = get_rotation_center(magenta_coords, valid_predicted_coords)
    rotated_grid, new_magenta_coords = rotate_magenta_object(output_grid, magenta_coords, center)
    output_grid = rotated_grid

    #set new magenta pixels - within bounds
    valid_new_magenta_coords = []
    for r,c in new_magenta_coords:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          output_grid[r,c] = 6
          valid_new_magenta_coords.append( (r,c) )


    # Adjust After Rotation
    adjust_after_rotation(output_grid, magenta_coords, valid_new_magenta_coords)


    return output_grid