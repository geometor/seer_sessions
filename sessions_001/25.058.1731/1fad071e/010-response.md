# 1fad071e • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1. Identify Blue Pixels: Locate all pixels with the value '1' (blue) in the input grid.
2. Count Blue Regions: Count the blue regions. If you view the blue pixels as connected to blue pixels that are to the left, right, top, or bottom of the blue pixel, the blue pixel form four distinct, not connected, regions.
3. Create Output: Generate a 1x5 grid. Place four blue pixels in a row followed by a single white pixel.

In essence, the transformation extracts and counts the disconnected regions of blue and represents it as a series of blue pixels, followed by a white pixel.
"""

import numpy as np

def get_connected_regions(grid, color):
    """
    Finds and counts connected regions of a specified color in a grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    count = 0

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                dfs(row, col)
                count += 1
    return count
    

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    # Count blue regions
    blue_regions_count = get_connected_regions(input_grid, 1)

    # Create output grid
    output_grid = np.zeros((1, blue_regions_count + 1), dtype=int)
    
    # Fill with blue pixels except for the last one
    output_grid[0, :blue_regions_count] = 1

    return output_grid
```
