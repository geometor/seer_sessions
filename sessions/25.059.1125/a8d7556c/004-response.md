# a8d7556c • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Gray Regions:** Find all contiguous regions of gray (5) pixels in the input grid. A contiguous region is defined as a group of gray pixels connected horizontally, vertically, or diagonally.

2.  **Select Gray Pixels for Replacement:** Within certain identified gray regions, select some gray pixels to be changed. The selection criteria will be some of the interior gray pixels.

3. **Change selected Pixel color:** Change the color of the select gray pixels identified for replacement to red (2).

4.  **Output:** The output grid is the same as the input grid, except for the gray pixels that have been replaced with red pixels. The choice for which gray areas and which pixels within gray areas are selected will take further analysis to identify the selection process.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        # Explore adjacent cells (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                region.extend(dfs(row + dr, col + dc))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                regions.append(dfs(row, col))

    return regions

def is_interior(grid, row, col, color):
    """Checks if a pixel is in the interior of a region of same color pixels"""

    #check that the cell is the correct color
    if grid[row,col] != color:
        return False
    
    # Check all 8 neighbors (including diagonals)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            
            #neighbor coordinates
            nr, nc = row + dr, col + dc
            
            #boundary check
            if (nr < 0 or nr >= grid.shape[0] or nc < 0 or nc >= grid.shape[1]
               or grid[nr,nc] != color):
                return False #if any neighbor is not the same color, its not interior
            

    return True # All neighbors passed, so it is interior


def transform(input_grid):
    """
    Transforms the input grid by replacing some interior gray pixels with red pixels.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    gray_regions = find_contiguous_regions(input_grid, 5)

    # Iterate over gray pixels and check if they should be replaced
    for region in gray_regions:
      for row, col in region:
          if is_interior(input_grid,row, col, 5):
              output_grid[row,col] = 2

    return output_grid
```
