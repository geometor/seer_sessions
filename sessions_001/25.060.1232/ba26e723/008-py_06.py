"""
The transformation rule identifies white pixels that function as corners of 3x3 yellow regions and changes these white pixels to magenta.
"""

import numpy as np

def find_yellow_regions(grid):
    """
    Identifies contiguous regions of yellow pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != 4):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 4 and not visited[i, j]:
                current_region = []
                dfs(i, j, current_region)
                regions.append(current_region)
    return regions

def is_corner(grid, row, col, yellow_regions):
    """
    Checks if a white pixel at (row, col) is a corner of a 3x3 yellow region.
    """
    if grid[row, col] != 0:
        return False

    for region in yellow_regions:
        for yellow_row, yellow_col in region:
            # Check for a potential 3x3 region
            if (abs(row - yellow_row) <= 2 and abs(col - yellow_col) <= 2):
                # Define the potential 3x3 region boundaries
                min_row = max(0, yellow_row - 1)  # Ensure within grid bounds
                max_row = min(grid.shape[0] -1, yellow_row + 1)
                min_col = max(0, yellow_col - 1)
                max_col = min(grid.shape[1] - 1, yellow_col + 1)

                # check if region is 3x3 using numpy
                area = grid[min_row:max_row+1, min_col:max_col+1]
                if area.shape == (3,3) and np.all(area == 4):
                  #check if row,col is one away from corners
                  if ((row == min_row - 1 or row == max_row + 1) and
                      (col == min_col - 1 or col == max_col + 1)):
                    return True

    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # find yellow areas
    yellow_regions = find_yellow_regions(input_grid)

    # change corner pixels to magenta
    for i in range(rows):
        for j in range(cols):
            if is_corner(output_grid, i, j, yellow_regions):
                output_grid[i, j] = 6

    return output_grid