"""
1.  **Identify the Largest Blue Object:** In the input grid, locate the largest contiguous "object" composed of blue (1) pixels. Contiguous means pixels are connected horizontally or vertically (not diagonally).
2.  **Create Bounding Box:** Find bounding box for this object.
3.  **Simplify to 3x3:** Project presence of blue cells into a 3x3 grid. If a cell in a relative section is blue, the new cell will be blue.
"""

import numpy as np

def find_largest_blue_object(grid):
    # helper to find the largest contiguous block of blue pixels
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_size = 0
    max_object_coords = []

    def dfs(r, c, current_object_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                (r, c) in visited or grid[r][c] != 1):
            return 0
        visited.add((r, c))
        current_object_coords.append((r,c))
        size = 1
        size += dfs(r + 1, c, current_object_coords)
        size += dfs(r - 1, c, current_object_coords)
        size += dfs(r, c + 1, current_object_coords)
        size += dfs(r, c - 1, current_object_coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                current_object_coords = []
                size = dfs(r, c, current_object_coords)
                if size > max_size:
                    max_size = size
                    max_object_coords = current_object_coords

    return max_object_coords

def bounding_box(coords):
    # helper to find the bounding box of a set of coordinates
    if not coords:
        return None
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in coords:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c, max_r, max_c)

def transform(input_grid):
    # Find the largest blue object
    largest_blue = find_largest_blue_object(input_grid)

    # get bounding box
    bbox = bounding_box(largest_blue)

    # init output
    output_grid = np.zeros((3, 3), dtype=int)

    if bbox:

        # map coordinates to 3x3 grid
        min_r, min_c, max_r, max_c = bbox

        height = max_r - min_r + 1
        width = max_c - min_c + 1

        for r,c in largest_blue:
          # use relative proportions to get the cell
          row_index = int(((r - min_r) / height) * 3)
          col_index = int(((c - min_c) / width) * 3)

          # fix bounds error
          row_index = min(row_index, 2)
          col_index = min(col_index, 2)
          output_grid[row_index, col_index] = 1

    return output_grid