"""
Objects move vertically, wrapping around the grid edges. The distance and direction
of movement appear to be specific to each individual object, not just its color.
Objects of the same color can move differently. The background can split.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid, including the background."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c]:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                if object_pixels:
                    objects.append({
                        'color': grid[r, c],
                        'pixels': object_pixels
                    })
    return objects

def calculate_object_shift(input_obj, output_objects, grid_height):
    """Calculates the vertical shift for a *single* input object."""

    # If the input object is background (color 0), don't shift
    if input_obj['color'] == 0:
      return 0

    input_rows = [r for r, _ in input_obj['pixels']]
    if not input_rows:
        return 0
    input_min_row = min(input_rows)

    # Find best match among output_objects
    best_match_shift = 0

    for output_obj in output_objects:

      if output_obj['color'] == input_obj['color']:
        output_rows = [r for r, _ in output_obj['pixels']]

        if not output_rows:
          continue;
        output_min_row = min(output_rows)

        shift = output_min_row - input_min_row
        return shift

    return best_match_shift #should not get here for non-background objects

def transform(input_grid, output_grid=None):
    # initialize output_grid
    output_grid_new = np.zeros_like(input_grid)

    if output_grid is None:
      return input_grid

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    # Calculate shifts for each input object

    # move objects based on shift
    for input_obj in input_objects:
        color = input_obj['color']
        shift = calculate_object_shift(input_obj, output_objects, input_grid.shape[0])
        for r, c in input_obj['pixels']:
            new_r = (r + shift) % input_grid.shape[0]  # Wrap around
            output_grid_new[new_r, c] = color

    return output_grid_new