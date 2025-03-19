"""
The color of the main shape in the output grid is determined by the color of the pixel in the bottom-left corner of the input grid. The shape itself is preserved; only the color changes.
"""

import numpy as np

def find_main_shape(grid):
    # Find the largest contiguous region of non-zero pixels.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_region = []
    max_region_color = 0

    def dfs(row, col, color, current_region):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row, col] != color:
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, color, current_region)
        dfs(row - 1, col, color, current_region)
        dfs(row, col + 1, color, current_region)
        dfs(row, col - 1, color, current_region)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_region = []
                color = grid[r, c]
                dfs(r, c, color, current_region)
                if len(current_region) > len(max_region):
                    max_region = current_region
                    max_region_color = color
    return max_region, max_region_color

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the main shape and its color
    main_shape_pixels, _ = find_main_shape(input_grid)

    # Find the color indicator
    color_indicator = input_grid[-1, 0]

    # change output pixels 
    for row, col in main_shape_pixels:
        output_grid[row, col] = color_indicator

    return output_grid