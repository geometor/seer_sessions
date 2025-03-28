# cf98881b • 026 • example_5 • investigate_coder

---
```python
"""
Extracts a subgrid from the input grid. The subgrid is defined by the bounding box of the largest contiguous yellow region, includes directly adjacent blue squares, and all other colors within this region are changed to white.
"""

import numpy as np

def find_largest_object(grid, color):
    # implementation of depth first search
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    max_object_coords = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return 0, []

        visited[row, col] = True
        size = 1
        coords = [(row, col)]

        # Explore all 8 neighbors (including diagonals).
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_size, new_coords = dfs(row + dr, col + dc)
                size += new_size
                coords.extend(new_coords)

        return size, coords

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                size, coords = dfs(r, c)
                if size > max_size:
                    max_size = size
                    max_object_coords = coords
    return max_object_coords

def get_bounding_box(coords):
    min_row = min(c[0] for c in coords)
    max_row = max(c[0] for c in coords)
    min_col = min(c[1] for c in coords)
    max_col = max(c[1] for c in coords)
    return min_row, max_row, min_col, max_col

def expand_bounding_box_for_blue(input_grid, bbox):
    min_row, max_row, min_col, max_col = bbox
    expanded_coords = []

    for r in range(min_row, max_row+1):
      for c in range(min_col, max_col+1):
        if input_grid[r,c] == 1: #blue
            #check neighbors to expand
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1]:
                      expanded_coords.append((nr,nc))

    if len(expanded_coords) > 0:
        er, ec, _, _ = get_bounding_box(expanded_coords)
        min_row = min(min_row, er)
        max_row = max(max_row, er)
        min_col = min(min_col, ec)
        max_col = max(max_col, ec)
    return  min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the largest yellow object.
    yellow_coords = find_largest_object(input_grid, 4)

    # Get its bounding box.
    bbox = get_bounding_box(yellow_coords)

    # expand for adjacent blue
    bbox = expand_bounding_box_for_blue(input_grid, bbox)
    min_row, max_row, min_col, max_col = bbox

    # Extract the subgrid.
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1].copy()

    # Replace colors other than yellow and blue with white within subgrid
    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] != 4 and output_grid[r,c] != 1:
          output_grid[r,c] = 0

    return output_grid
```
