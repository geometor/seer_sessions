"""
1. Check for the presence of distinct regions of yellow(4) pixels within a
   background of white(0).
2. If there are multiple, non-adjacent regions of color 4, return a blank
   output `[[]]`.
2. Otherwise, identify yellow (4) pixels.
3.  Discard pixels of colors white(0) or gray(5).
4. Create a Bounding Subgrid: Find the smallest rectangular subgrid in the original input
   that contains all the yellow pixels.
5. Extract Subgrid: Extract and return the minimal bounding subgrid containing yellow.
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
    # Find coordinates of all pixels with the target color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # No pixels of the target color found

    # Find min and max row and col
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid based on the presence and arrangement of yellow pixels.
    """
    input_grid = np.array(input_grid)
    target_color = 4

    # 1. Check for distinct regions of yellow pixels.
    regions = get_regions(input_grid, target_color)

    # 2. Return blank output if multiple non-adjacent regions.
    if len(regions) > 1:
          return [[]]

    # 3 & 4 Create Bounding subgrid
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid, target_color)
    
    if min_row is None: # Handle cases of no target color
       return [[]]

    # 5. Extract Subgrid
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    return output_grid.tolist()