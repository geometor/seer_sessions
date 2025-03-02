"""
Recolor specific regions within the input grid. Regions of color '4' (yellow) are changed to '3' (green),
and regions of color '8' (light blue) are changed to '9'(maroon). The transformation appears to be spatially determined,
affecting regions that are towards the lower right corner of the grid.
"""

import numpy as np

def find_regions_by_color(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.
    Returns a list of sets, where each set contains the (row, col) coordinates of a region.
    """
    rows, cols = grid.shape
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.add((row, col))
        # Explore adjacent cells
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = set()
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find regions of color '4' (yellow)
    yellow_regions = find_regions_by_color(output_grid, 4)
    
    # Recolor yellow regions to '3' (green)
    for region in yellow_regions:
        for row, col in region:
            output_grid[row, col] = 3

    # Find regions of color '8' (light blue)
    light_blue_regions = find_regions_by_color(output_grid, 8)

    # Recolor light blue regions to '9' (maroon)
    for region in light_blue_regions:
        for row, col in region:
            output_grid[row,col] = 9

    return output_grid