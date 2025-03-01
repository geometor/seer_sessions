# c8cbb738 • 004 • refine_coder

---
```python
"""
Transforms an input grid by extracting the largest contiguous region of non-background color and using it as the output grid.
"""

import numpy as np
from collections import Counter

def get_dominant_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def find_object(grid, target_color):
    """Finds the largest contiguous region of the target color."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    max_region = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                grid[row][col] != target_color or (row, col) in visited):
            return
        visited.add((row, col))
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == target_color and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                if len(current_region) > len(max_region):
                    max_region = current_region
    return max_region


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the background (dominant) color.
    dominant_color = get_dominant_color(input_grid)

    # 2. Check if the grid is uniform.
    if np.all(input_grid == dominant_color):
        return input_grid.tolist()  # Return input unchanged

    # 3. Find the largest object of non-background color
    target_colors = set(input_grid.flatten())
    target_colors.discard(dominant_color)

    # Find largest object amongst all target colors
    largest_object = []
    for color in target_colors:
        object_coords = find_object(input_grid, color)
        if len(object_coords) > len(largest_object):
            largest_object = object_coords

    # find min/max row/col
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r,c in largest_object:
      if r < min_row:
        min_row = r
      if c < min_col:
        min_col = c
      if r > max_row:
        max_row = r
      if c > max_col:
        max_col = c
        
    # 4. Create Output Grid based on the object dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.full((output_height, output_width), dominant_color) # initialize
    
    # 5. Fill the output grid
    for row, col in largest_object:
        output_grid[row - min_row, col - min_col] = input_grid[row, col]


    return output_grid.tolist()
```
