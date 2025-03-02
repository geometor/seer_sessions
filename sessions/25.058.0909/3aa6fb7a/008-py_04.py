"""
Identifies contiguous regions of azure (8) pixels in the input grid. 
Then, it changes a subset of these azure pixels to blue (1) based on an internal line-tracing logic.
The original grid dimensions and the positions of unchanged pixels are preserved.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions (objects) of a specific color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

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
                regions.append(dfs(row, col))

    return regions

def select_pixels_to_change(region):
    """
    Selects a subset of pixels within a region to be changed, implementing a simplified
    line-tracing-like logic.  This is a placeholder for a more complex rule.
    It selects the pixel after the first on the top left for change.
    """
    # Sort the region by row and then by column
    sorted_region = sorted(region, key=lambda x: (x[0], x[1]))
    pixels_to_change = []
    
    if (len(sorted_region) > 1):
      pixels_to_change.append(sorted_region[1])

    return pixels_to_change

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find contiguous regions of azure (8) pixels
    azure_regions = find_contiguous_regions(input_grid, 8)

    # Iterate through each azure region
    for region in azure_regions:
        # Select pixels to change based on the simplified line-tracing logic
        pixels_to_change = select_pixels_to_change(region)

        # Change the color of selected pixels to blue (1)
        for row, col in pixels_to_change:
            output_grid[row, col] = 1

    return output_grid