"""
Replaces gray (5) regions in the input grid with a symmetrical pattern of blue (1), red (2), and yellow (4) pixels, while preserving white (0) regions. The pattern within each gray region alternates colors in layers: blue, yellow, red, red, yellow, blue and repeats. The layers are concentric, filling the gray region from the outside in.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of contiguous gray regions in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != 5
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 5 and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform_region(grid, region):
    """
    Transforms a single gray region into concentric layers of colors.
    """
    output_region = np.copy(grid)
    color_sequence = [1, 4, 2, 2, 4, 1]
    layer = 0
    region_set = set(region)  # Convert to set for faster lookups

    while region_set:
        color = color_sequence[layer % len(color_sequence)]
        border_pixels = set()

        # Find the current border pixels
        for r, c in region_set:
            neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
            for nr, nc in neighbors:
                if (nr, nc) not in region_set:
                    border_pixels.add((r,c))
                    break

        # Fill border pixels with the current color
        for r, c in border_pixels:
            output_region[r, c] = color

        # Remove border pixels from the region set for next iteration
        region_set -= border_pixels
        layer += 1

    return output_region

def transform(input_grid):
  """
  transform the input to match the output by replacing grey regions with
  concentric colored layers.
  """
    # initialize output_grid
  output_grid = np.copy(input_grid)

    # get list of grey objects
  gray_regions = get_objects(input_grid)

    # return unchanged if no grey objects
  if (len(gray_regions) == 0):
    return output_grid

    # transform grey objects
  for region in gray_regions:
      output_grid = transform_region(output_grid, region)
        

  return output_grid