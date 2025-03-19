# 6a1e5592 • 004 • example_1 • investigate_coder

---
```python
"""
Replaces gray pixels with white and white pixels enclosed by red pixels with blue.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_inside_outline(pixel, outline_pixels, grid_shape):
    """
    Checks if a pixel is inside a contiguous outline using a ray-casting approach.
    Considers points on the edges to be *not* contained.
    """
    row, col = pixel
    crossings = 0

    # count edge transitions of the pixel
    for r, c in outline_pixels:
       if r==row and c==col: # pixel is part of outline
           return False

    # Test only to the right, optimized since red outline is on the right
    for c in range(col + 1, grid_shape[1]):
      if (row,c) in outline_pixels:
        crossings += 1

    # odd number of crossings means it is within the outline
    return crossings % 2 == 1


def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Replace all gray (5) pixels with white (0)
    output_grid[output_grid == 5] = 0
    
    # Find contiguous regions of red pixels
    red_regions = find_contiguous_regions(output_grid, 2)
    
    red_outline_pixels = set()
    for region in red_regions:
        red_outline_pixels.update(region)

    # Find white pixels inside red outline
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == 0:  # if it is a white pixel
                if is_inside_outline((row,col), red_outline_pixels, output_grid.shape):
                    output_grid[row, col] = 1 # set to blue
    
    return output_grid
```
