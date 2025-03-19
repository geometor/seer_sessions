# 48d8fb45 • 014 • refine_coder

---
```python
"""
1. Identify Yellow and Gray Regions: Find all contiguous regions of yellow (4) and gray (5) pixels in the input grid.
2. Check for Single Yellow Region: If there is more than one distinct yellow region, return a blank grid (`[[]]`).
3. Determine Bounding Box: If there's a single yellow region, find its bounding box (the smallest rectangle containing all yellow pixels).
4. Gray Pixel Inclusion:
    - Extract the subgrid defined by the yellow region's bounding box *including* any padding.
    - Check if the gray pixels within this subgrid, form a *single contiguous region*.
    - remove any white(0) padding from the edges
5. Extract and Crop: Return the extracted subgrid, with the white padding removed.
"""

import numpy as np

def get_regions(grid, color):
    """Finds distinct regions of the specified color."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col):
        """Depth-first search to find connected regions."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == color:
                regions.append(dfs(row, col))
    return regions

def get_bounding_box(grid, color):
    """Finds the bounding box of the specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # No pixels of the target color found

    # Find min and max row and col
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()

    return min_row, max_row, min_col, max_col

def remove_padding(grid, color=0):
    """Removes padding of the specified color from the edges of a grid."""
    rows = np.any(grid != color, axis=1)
    cols = np.any(grid != color, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    return grid[rmin:rmax+1, cmin:cmax+1]
    

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    yellow_color = 4
    gray_color = 5

    # 1. Identify Yellow and Gray Regions
    yellow_regions = get_regions(input_grid, yellow_color)
    gray_regions = get_regions(input_grid, gray_color)

    # 2. Check for Single Yellow Region
    if len(yellow_regions) > 1:
        return [[]]

    # 3. Determine Bounding Box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid, yellow_color)
    if min_row is None:  # Handle cases with no yellow pixels
        return [[]]

    # 4. Gray Pixel Inclusion and Padding Removal
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    gray_regions_subgrid = get_regions(subgrid, gray_color)
    if len(gray_regions_subgrid) > 1:
        #remove grey if there are multiple grey regions
        subgrid[subgrid == gray_color] = 0
        
    
    output_grid = remove_padding(subgrid)


    return output_grid.tolist()
```
