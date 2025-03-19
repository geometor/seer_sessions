# 868de0fa • 032 • refine_coder

---
```python
"""
1.  **Identify Enclosed Regions:** Find all enclosed regions formed by contiguous blue (1) pixels.
2.  **Determine Fill Color:** Each enclosed region has a unique and consistent fill color. There are no divider lines within shapes.
    *   The first identified enclosed region (from top-left, reading row-wise) is filled with orange (7).
    *   The second identified enclosed region is filled with red (2).
    *   The third and subsequent regions alternate - orange and then red
3.  **Fill Enclosed Regions:** For each identified enclosed region, replace all interior white (0) pixels with the designated fill color determined in step 2.
4.  **Preserve Outlines:** Keep the original blue pixels of the outline unchanged.
"""

import numpy as np

def find_shapes(grid, outline_color):
    # Find all outline pixels
    outline_pixels = np.where(grid == outline_color)
    shapes = []
    visited = set()

    def is_valid(x, y):
        return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

    def dfs(x, y, current_shape):
        if (x, y) in visited or not is_valid(x, y) or grid[x, y] != outline_color:
            return
        visited.add((x, y))
        current_shape.append((x, y))

        # Explore adjacent pixels
        dfs(x + 1, y, current_shape)
        dfs(x - 1, y, current_shape)
        dfs(x, y + 1, current_shape)
        dfs(x, y - 1, current_shape)


    for x, y in zip(*outline_pixels):
        if (x, y) not in visited:
            current_shape = []
            dfs(x, y, current_shape)
            shapes.append(current_shape)
    return shapes

def flood_fill(grid, x, y, fill_color, outline_color):
    # classic flood fill algorithm

    if not (0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]):
        return
    if grid[x, y] == outline_color or grid[x,y] == fill_color:
        return

    grid[x, y] = fill_color
    flood_fill(grid, x + 1, y, fill_color, outline_color)
    flood_fill(grid, x - 1, y, fill_color, outline_color)
    flood_fill(grid, x, y + 1, fill_color, outline_color)
    flood_fill(grid, x, y - 1, fill_color, outline_color)

def fill_region(grid, shape, fill_color, outline_color):
    # Fill a single enclosed region with the specified color
    min_x = min(x for x, y in shape)
    max_x = max(x for x, y in shape)
    min_y = min(y for x, y in shape)
    max_y = max(y for x, y in shape)

    for x in range(min_x + 1, max_x):
        for y in range(min_y + 1, max_y):
            if grid[x, y] != outline_color:
                flood_fill(grid, x, y, fill_color, outline_color)


def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find shapes outlined in blue (1)
    blue_shapes = find_shapes(input_grid, 1)

    # Determine and apply fill colors
    fill_colors = [7, 2]  # Orange, then Red
    color_index = 0
    
    for shape in blue_shapes:
        fill_color = fill_colors[color_index % len(fill_colors)]
        fill_region(output_grid, shape, fill_color, 1)
        color_index += 1

    return output_grid
```
