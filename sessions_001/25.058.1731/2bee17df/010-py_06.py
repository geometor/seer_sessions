"""
Identifies the largest white (0) region within the input grid that forms a cross shape, 
bordered by red (2) pixels, and replaces this region with green (3) pixels. 
All other pixels remain unchanged.
"""

import numpy as np

def get_contiguous_regions(grid, color):
    """
    Finds all contiguous regions of a specific color in the grid.
    Returns a list of sets, where each set contains the (row, col) coordinates of a contiguous region.
    """
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] != color
            or (row, col) in visited
        ):
            return
        visited.add((row, col))
        current_region.add((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = set()
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_cross_shaped(region, grid):
    """
    Checks if a region is cross-shaped, extending to red (2) borders on all four sides.
    """
    if not region:
        return False

    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Check for red borders around the bounding box of the region
    for row in range(min_row, max_row + 1):
        #check if left and right has red
        if not any(grid[row,c] == 2 for c in range(0,min_col)):
            return False

        if not any(grid[row,c] == 2 for c in range(max_col+1, grid.shape[1])):
            return False

    for col in range(min_col, max_col+1):
        # Check top
        if not any(grid[r,col] == 2 for r in range(0,min_row)):
            return False
        if not any(grid[r, col] == 2 for r in range(max_row + 1, grid.shape[0])):
              return False
    return True

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    # Find all contiguous regions of white pixels
    white_regions = get_contiguous_regions(input_grid, 0)

    # Find the cross shaped region
    cross_shaped_region = None

    for region in white_regions:
      if is_cross_shaped(region, input_grid):
          cross_shaped_region = region
          break
    
    # If found cross region, change color
    if cross_shaped_region is not None:
          for row, col in cross_shaped_region:
              output_grid[row, col] = 3


    return output_grid