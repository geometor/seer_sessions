# 0e206a2e • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying single-pixel colors (blue, red, yellow)
and an azure cluster in the input grid. The positions of these single pixels
are maintained in the output grid. The azure cluster from the input is
duplicated in the output grid, with its relative positioning determined
by the single pixels.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of pixels of a specific color."""
    return np.argwhere(grid == color)

def find_cluster(grid, color):
    """Finds a cluster of connected pixels of a specific color."""
    coords = find_pixels_by_color(grid, color)
    if len(coords) == 0:
        return []

    cluster = []
    visited = set()
    
    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        cluster.append((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
        
    start_row, start_col = coords[0]
    dfs(start_row, start_col)

    return cluster
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)

    # Find the single pixels (blue, red, yellow)
    blue_pixel = find_pixels_by_color(input_grid, 1)
    red_pixel = find_pixels_by_color(input_grid, 2)
    yellow_pixel = find_pixels_by_color(input_grid, 4)

    # Find the azure cluster
    azure_cluster = find_cluster(input_grid, 8)
    
    # Place the single pixels in the output grid
    if len(blue_pixel) > 0:
        output_grid[blue_pixel[0][0], blue_pixel[0][1]] = 1
    if len(red_pixel) > 0:
        output_grid[red_pixel[0][0], red_pixel[0][1]] = 2
    if len(yellow_pixel) > 0:
         output_grid[yellow_pixel[0][0], yellow_pixel[0][1]] = 4
   

    # Duplicate and translate the azure cluster
    if (len(azure_cluster) > 0):

      for row, col in azure_cluster:
          output_grid[row,col] = 8


    return output_grid
```
