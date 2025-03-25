```python
"""
Replaces gray (5) regions in the input grid with a symmetrical pattern of blue (1), red (2), and yellow (4) pixels, while preserving white (0) regions. The pattern within each gray region alternates colors in layers: blue, yellow, red, red, yellow, blue and repeats.
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
      transform the region to use repeating, inward color bands
    """

    # make a copy, operates on the copy, the original is updated later
    output_region = np.copy(grid)

    min_row = min(r for r, c in region)
    max_row = max(r for r, c in region)
    min_col = min(c for r, c in region)
    max_col = max(c for r, c in region)

    
    color_sequence = [1, 4, 2, 2, 4, 1]  # Blue, Yellow, Red, Red, Yellow, Blue
    layer = 0

    while min_row <= max_row and min_col <= max_col:
        color = color_sequence[layer % len(color_sequence)]

        # Top and bottom borders
        for col in range(min_col, max_col + 1):
            if (min_row, col) in region:
                output_region[min_row, col] = color
            if (max_row, col) in region:
                output_region[max_row, col] = color


        # Left and right borders
        for row in range(min_row + 1, max_row):
            if (row, min_col) in region:
             output_region[row, min_col] = color
            if (row, max_col) in region:
             output_region[row, max_col] = color
        
        # update bounds for next layer
        min_row += 1
        max_row -= 1
        min_col += 1
        max_col -= 1
        layer += 1

    return output_region


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # get list of grey objects
    gray_regions = get_objects(input_grid)
    
    # return unchanged if no grey objects
    if (len(gray_regions) == 0):
      return output_grid

    # transform grey objects
    first = True
    for region in gray_regions:
        if (first):
          output_grid = transform_region(output_grid, region)
          first = False
        else:
          # all subsequent regions must be applied to the latest output
          output_grid = transform_region(output_grid, region)

    return output_grid
```