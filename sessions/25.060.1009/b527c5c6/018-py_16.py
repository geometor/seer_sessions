"""
The program identifies green regions in the input grid. If a green region contains a red pixel, the region is expanded upwards. The expansion fills all pixels with green within the column bounds of the original green region, from the top of the grid down to and including the row containing the highest red pixel within that region.  Pixels in the input grid not modified by this expansion are preserved.
"""

import numpy as np

def find_objects_by_color(grid, color):
    """Find connected regions of a specific color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col):
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
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))

    return objects

def find_highest_red_pixel(grid, region):
    """Find the highest row index of a red pixel within a given region."""
    highest_row = float('inf')
    for row, col in region:
        if grid[row, col] == 2:
            highest_row = min(highest_row, row)
    return highest_row if highest_row != float('inf') else None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find green regions
    green_regions = find_objects_by_color(input_grid, 3)
    
    # Iterate through each green region
    for region in green_regions:
        # Find the highest red pixel within the region
        highest_red_row = find_highest_red_pixel(input_grid, region)
        
        # If a red pixel is found, perform the expansion
        if highest_red_row is not None:
            # Determine column bounds of the region
            min_col = min([c for r, c in region])
            max_col = max([c for r, c in region])
            
            # Fill with green from the top to the red pixel's row
            for row in range(highest_red_row + 1):  # +1 to include the red pixel's row
                for col in range(min_col, max_col + 1):
                    output_grid[row, col] = 3

    return output_grid