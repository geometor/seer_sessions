# a85d4709 • 018 • refine_coder

---
```python
"""
Transforms the input grid according to the following rules:
1. All gray pixels become red.
2. If the grid has odd dimensions, the center pixel (if white) becomes yellow.
3. Identify the contiguous white region around the center pixel (if it exists). This region includes all directly or diagonally connected white pixels.
4. All white pixels directly adjacent to the center are converted to yellow.
5. All other white pixels (not part of the central white region) become red.
6. If the grid has even dimensions, only rules 1 and 5 apply.
"""

import numpy as np

def get_center(grid):
    rows, cols = grid.shape
    if rows % 2 != 0 and cols % 2 != 0:
        return rows // 2, cols // 2
    return None

def get_contiguous_region(grid, start_row, start_col, color):
    rows, cols = grid.shape
    visited = set()
    region = []
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        region.append((r, c))
        # Explore 8-connectivity (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc)

    dfs(start_row, start_col)
    return region

def get_adjacent_pixels(grid, row, col):
    rows, cols = grid.shape
    adjacent = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                adjacent.append((new_row,new_col))
    return adjacent

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Gray to Red
    output_grid[output_grid == 5] = 2

    # 2 & 3. Center pixel and contiguous region (for odd dimensions)
    center = get_center(output_grid)
    if center:
        center_row, center_col = center
        #Center to Yellow
        if output_grid[center_row, center_col] == 0:
          output_grid[center_row, center_col] = 4
          #4. Surrounding White to Yellow
          adjacent_pixels = get_adjacent_pixels(output_grid, center_row, center_col)
          for r, c in adjacent_pixels:
            if output_grid[r,c] == 0:
              output_grid[r,c] = 4
        # Identify Central White Region
        central_white_region = get_contiguous_region(output_grid, center_row, center_col, 0)


        # 5. Other White to Red
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 0 and (r, c) not in central_white_region:
                    output_grid[r, c] = 2
    else: #even grid
        # 5. Other White to Red (for even dimensions)
        output_grid[output_grid == 0] = 2
    return output_grid
```
