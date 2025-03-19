# 846bdb03 • 024 • refine_coder

---
```python
"""
The input grid is transformed into a smaller output grid by extracting and simplifying colored regions. Yellow (4) regions are reduced to their corner pixels. Orange (7) and Green (3) regions are merged if vertically adjacent or overlapping, and then filled. The final output grid is condensed by finding the bounding boxes for each simplified region.
"""

import numpy as np

def get_regions(grid, color):
    regions = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(row, col):
        if (row, col) in visited or not is_valid(row, col) or grid[row, col] != color:
            return []

        visited.add((row, col))
        region = [(row, col)]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            region.extend(dfs(row + dr, col + dc))
        
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color and (r,c) not in visited:
                regions.append(dfs(r,c))

    return regions

def get_corners(region):
    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    top_left = (min_row, min_col)
    top_right = (min_row, max_col)
    bottom_left = (max_row, min_col)
    bottom_right = (max_row, max_col)

    corners = set()
    if top_left in region:
        corners.add(top_left)
    if top_right in region:
        corners.add(top_right)
    if bottom_left in region:
        corners.add(bottom_left)
    if bottom_right in region:
        corners.add(bottom_right)
    return list(corners)

def get_bounding_box(region):
    if not region:
        return None  # Handle empty regions

    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col


def transform(input_grid):
    # 1. Identify Colored Regions.
    yellow_regions = get_regions(input_grid, 4)
    orange_regions = get_regions(input_grid, 7)
    green_regions = get_regions(input_grid, 3)

    # 2. Simplify Yellow Regions (Corners).
    simplified_yellow = []
    for region in yellow_regions:
        simplified_yellow.extend(get_corners(region))

    # 3. Combine Orange and Green regions
    combined_orange_green = []
    for region in orange_regions:
        combined_orange_green.extend(region)
    for region in green_regions:
        combined_orange_green.extend(region)

    # 4. Create bounding boxes
    yellow_bounding_box = get_bounding_box(simplified_yellow)
    orange_green_bounding_box = get_bounding_box(combined_orange_green)
    
    boxes = []
    if yellow_bounding_box:
      boxes.append(yellow_bounding_box)
    if orange_green_bounding_box:
      boxes.append(orange_green_bounding_box)

    if not boxes:
      return np.zeros((0,0), dtype=int)
    
    # find the min and max of the combined boxes:
    min_rows, max_rows, min_cols, max_cols = zip(*boxes)
    min_row = min(min_rows)
    max_row = max(max_rows)
    min_col = min(min_cols)
    max_col = max(max_cols)    
    
    # 5. Create Output Grid
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
        
    # 6. Populate output grid
    for r, c in simplified_yellow:
        output_grid[r - min_row, c - min_col] = 4
    
    # fill combined regions
    if combined_orange_green:
        
        # fill based on the bounding box of the combined region
        orange_green_rows, orange_green_cols = zip(*combined_orange_green)
        min_og_row = min(orange_green_rows)
        max_og_row = max(orange_green_rows)
        min_og_col = min(orange_green_cols)
        max_og_col = max(orange_green_cols)
        
        for r in range(min_og_row, max_og_row+1):
            for c in range(min_og_col, max_og_col+1):
                if (r,c) in combined_orange_green:
                    color = input_grid[r,c] # original color
                    output_grid[r - min_row, c- min_col] = color

    # 7. Return Output Grid
    return output_grid
```
