"""
Moves one gray pixel to a position adjacent to a red object, and removes other gray pixels.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.argwhere(grid == color).tolist()

def find_adjacent_empty(grid, object_pixels):
    # Find an empty cell adjacent to any of the object pixels.
    rows, cols = grid.shape
    for r, c in object_pixels:
        # Check adjacent cells (up, down, left, right).
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                return (nr, nc)
    return None

def distance(pos1, pos2):
    # Manhattan distance
    return abs(pos1[0] - pos2[0]) + abs(pos1[1]-pos2[1])


def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find gray pixels.
    gray_pixels = find_objects(input_grid, 5)

    # Find red pixels.
    red_pixels = find_objects(input_grid, 2)

    if not red_pixels or not gray_pixels:
        return output_grid # No change if no red or grey pixels

    # Determine the target position (adjacent empty cell).
    target_pos = find_adjacent_empty(output_grid, red_pixels)


    # Move one gray pixel to the target position and remove the others
    if target_pos:
        # find closest grey pixel
        min_dist = float('inf')
        closest_grey = None
        for grey in gray_pixels:
            d = distance(target_pos, grey)
            if d < min_dist:
                min_dist = d
                closest_grey = grey
        if closest_grey:
          # Move one gray pixel
          old_r, old_c = closest_grey
          output_grid[target_pos[0], target_pos[1]] = 5  # Move to target position
          output_grid[old_r, old_c] = 0  # clear old position


    # Remove any other gray pixels
    for i in range(len(gray_pixels)):
      if gray_pixels[i] != closest_grey:
        old_r, old_c = gray_pixels[i]
        output_grid[old_r, old_c] = 0

    return output_grid