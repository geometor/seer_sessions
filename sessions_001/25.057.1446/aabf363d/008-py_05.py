"""
The transformation identifies a contiguous shape of green (3) pixels and replaces it with an identical shape of magenta (6) pixels. A single magenta (6) pixel in the input acts as a "seed" or indicator for the replacement color, and this seed pixel itself is turned to white(0) in the output. All other white (0) pixels remain unchanged.
"""

import numpy as np

def find_contiguous_shape(grid, color):
    # Find the contiguous shape of a given color
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shape_pixels = []

    def dfs(row, col):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        shape_pixels.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                dfs(r, c)
                return shape_pixels  # Return as soon as the first shape is found
    return []

def find_seed_pixel(grid, color):
  # Find a single pixel of the specified color
  rows, cols = grid.shape
  for r in range(rows):
    for c in range(cols):
        if grid[r,c] == color:
            return (r, c)
  return None
    

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the seed pixel (magenta/6)
    seed_pixel = find_seed_pixel(input_grid, 6)

    # Find the contiguous shape of green (3) pixels
    green_shape_pixels = find_contiguous_shape(input_grid, 3)

    # Replace the green shape with magenta in the output grid
    for row, col in green_shape_pixels:
        output_grid[row, col] = 6
    
    # remove seed pixel by changing to white
    if seed_pixel:
      output_grid[seed_pixel] = 0

    return output_grid