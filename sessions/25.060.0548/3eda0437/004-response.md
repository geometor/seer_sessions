# 3eda0437 • 004 • refine_coder

---
```python
"""
1.  **Identify White Regions:** Find all contiguous regions of white (0) pixels in the input grid. A region is defined as one or more adjacent white pixels. Adjacency includes horizontal and vertical neighbors, but not diagonal ones.

2. **Check for specific Adjacency:** Iterate through each identified white region. For each region, check if it has azure colored pixels to the immediate right or bottom.

3.  **Fill with Magenta:** If a white region is adjacent to azure on the right or bottom, change all pixels within that white region to magenta (6).

4.  **Output:** The output grid is the result of applying these transformations to the input grid.
"""

import numpy as np

def get_contiguous_white_regions(grid):
    """
    Finds contiguous regions of white (0) pixels in the grid.
    Returns a list of lists, where each inner list contains the (row, col) coordinates of a white region.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    white_regions = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_region):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 0:
            return
        visited[r, c] = True
        current_region.append((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                white_regions.append(current_region)
    return white_regions

def is_adjacent_to_azure(grid, region):
    """
    Checks if a given region is adjacent to an azure (1) pixel on the right or bottom.
    """
    rows, cols = grid.shape
    for r, c in region:
        # Check right
        if c + 1 < cols and grid[r, c + 1] == 1:
            return True
        # Check bottom
        if r + 1 < rows and grid[r + 1, c] == 1:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify White Regions
    white_regions = get_contiguous_white_regions(input_grid)

    # Check for specific Adjacency and Fill
    for region in white_regions:
        if is_adjacent_to_azure(input_grid, region):
            for r, c in region:
                output_grid[r, c] = 6

    return output_grid
```
