# 44d8ac46 • 006 • refine_coder

---
```python
"""
The transformation identifies connected regions of gray pixels in the input grid and fills them with red.
Isolated gray regions that do not share a border with other gray regions remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the valid neighbors of a cell in a grid (up, down, left, right).
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill on the grid starting from (row, col).
    """
    if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]:
        return  # Out of bounds
    if grid[row, col] != target_color:
        return  # Not the target color

    grid[row, col] = replacement_color
    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        flood_fill(grid, r, c, target_color, replacement_color)

def transform(input_grid):
    """
    Transforms the input grid by filling connected gray regions with red.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    gray_regions = []

    # 1. Identify Gray Regions and store them
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5 and not visited[row, col]:
                # New gray region found, use flood fill to get the extent
                region_mask = np.zeros_like(output_grid, dtype=bool)
                flood_fill(region_mask, row, col, 1, 1) # Use 1 and -1 for flood fill temporary
                
                current_region = []
                for r in range(rows):
                    for c in range(cols):
                        if region_mask[r,c] == True:
                            current_region.append((r,c))
                            visited[r,c] = True
                gray_regions.append(current_region)

    # 2. Check for Connectivity
    connected = False
    for i in range(len(gray_regions)):
      for j in range(i + 1, len(gray_regions)):
        for r1, c1 in gray_regions[i]:
          for r2, c2 in gray_regions[j]:
            if (abs(r1 - r2) == 1 and c1 == c2) or \
               (abs(c1 - c2) == 1 and r1 == r2): # adjacent
                connected = True
                break
          if connected:
            break
        if connected:
            break

    # 3. Fill Connected Regions or Isolated
    for region in gray_regions:
        if connected:
          for r, c in region:
            output_grid[r, c] = 2  # Change to red
    return output_grid
```
