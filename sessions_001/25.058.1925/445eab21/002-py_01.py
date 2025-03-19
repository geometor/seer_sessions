"""
The output is a 2x2 square of pixels that has the same color as the larger L-shaped object in the input.
"""

import numpy as np

def find_l_shape(grid):
    # Find the largest contiguous block of non-white pixels forming an "L" shape.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    l_color = 0

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return 0
        visited[r, c] = True
        size = 1
        size += dfs(r + 1, c, color)
        size += dfs(r - 1, c, color)
        size += dfs(r, c + 1, color)
        size += dfs(r, c - 1, color)
        return size

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r,c]
                size = dfs(r, c, color)
                if size > max_size:
                    max_size = size
                    l_color = color

    return l_color
                

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((2, 2), dtype=int)

    # Find the color of the L-shape
    l_color = find_l_shape(input_grid)

    # Color the output grid with the L-shape's color.
    output_grid[:] = l_color

    return output_grid