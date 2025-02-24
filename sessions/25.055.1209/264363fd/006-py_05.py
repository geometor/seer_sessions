"""
The transformation identifies blue (1) regions within the input grid. For each blue region, it creates an "inner border" of red (2) pixels. An inner border pixel is a blue pixel that is adjacent (horizontally or vertically) to at least one non-blue pixel.  Within this inner border, "corner" pixels are highlighted in green (3). A corner pixel is an inner border pixel that is adjacent (horizontally, vertically, or diagonally) to at least two pixels that are not blue.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c),
                                      (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def get_inner_border(grid, obj):
    # Find pixels within the object that border a pixel of a different color
    rows, cols = grid.shape
    inner_border = []
    for r, c in obj:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr, nc] != 1:
                inner_border.append((r,c))
                break # move to next pixel in obj once one border is found
    return inner_border

def is_corner(grid, r, c, obj):

    rows, cols = grid.shape
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # skip the current cell

            nr, nc = r + dr, c + dc
            # condition: within bounds and different color
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr,nc] != 1:
                    count += 1
            elif not(0 <= nr < rows and 0 <= nc < cols):
                # count out of bounds as different
                count = count + 1

    return count >= 2

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find blue objects.
    blue_objects = find_objects(input_grid, 1)

    # Create inner borders and highlight corners.
    for obj in blue_objects:
        inner_border = get_inner_border(input_grid, obj)
        for r, c in inner_border:
          output_grid[r,c] = 2
          if is_corner(input_grid, r, c, obj):
              output_grid[r, c] = 3

    return output_grid