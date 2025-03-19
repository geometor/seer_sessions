"""
Removes contiguous regions of white pixels (value 0) from the input grid, 
preserving the positions of all other colored pixels.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specified color in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """
        Depth-First Search helper to explore contiguous regions.
        """
        if (row < 0 or row >= grid.shape[0] or
            col < 0 or col >= grid.shape[1] or
            visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_region.append((row, col))

        # Explore adjacent cells
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)

    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing contiguous white regions.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = input_grid.copy()

    # Find contiguous regions of white pixels (color 0)
    white_regions = find_contiguous_regions(output_grid, 0)

    # Iterate through the white regions and set those pixels to be removed
    for region in white_regions:
        for row, col in region:
            # Ensure the pixel is within array bounds (defensive check)
            if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                output_grid[row, col] = 0 # just keep it as is

    return output_grid