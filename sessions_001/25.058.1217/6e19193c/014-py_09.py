"""
1.  **Identify Maroon Pixels:** Locate all maroon (9) pixels in the input grid.
2.  **Edge Check and Reflect:** If a maroon pixel is a single pixel, and is on the edge of the grid, then reflect that pixel to the opposite edge of its row or column.
3.  **Preserve Background:** All non-maroon (background) pixels remain unchanged.
4. If a cluster is not along the edge, do not change.
"""

import numpy as np

def find_maroon_pixels(grid):
    # Find coordinates of all maroon pixels
    return np.argwhere(grid == 9)

def is_single_pixel(grid, r, c):
    # check if it is part of cluster
    count = 0
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 9:
                count += 1
    return count == 0

def is_on_edge(grid, r, c):
    # Check if a pixel is on the edge of the grid
    return r == 0 or r == grid.shape[0] - 1 or c == 0 or c == grid.shape[1] - 1

def reflect_pixel(grid, r, c):
    # Reflect a single pixel to the opposite edge
    new_r, new_c = r, c
    if r == 0:
        new_r = grid.shape[0] - 1
    elif r == grid.shape[0] - 1:
        new_r = 0
    if c == 0:
        new_c = grid.shape[1] - 1
    elif c == grid.shape[1] - 1:
        new_c = 0
    return new_r, new_c

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = input_grid.copy()
    maroon_pixels = find_maroon_pixels(input_grid)

    for r, c in maroon_pixels:
      if is_single_pixel(input_grid,r,c) and is_on_edge(input_grid, r, c):
        new_r, new_c = reflect_pixel(input_grid, r, c)
        output_grid[new_r, new_c] = 9

    return output_grid