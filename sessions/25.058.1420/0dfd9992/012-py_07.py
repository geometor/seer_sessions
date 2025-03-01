"""
Removes large contiguous white regions from the input grid.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a specific color in the grid.

    Args:
        grid: The input grid (2D numpy array).
        color: The color to search for.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a contiguous region.
    """
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.add((row, col))
        # Check neighbors (up, down, left, right)
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

def transform(input_grid):
    """
    Transforms the input grid by removing large contiguous white regions.

    Args:
        input_grid: The input grid (2D numpy array).

    Returns:
        The transformed grid (2D numpy array).
    """
    grid = np.array(input_grid)  # Convert to numpy array for easier manipulation
    output_grid = np.copy(grid)  # Start with a copy of the input grid
    
    white_regions = find_contiguous_regions(grid, 0)

    # Iterate through the identified white regions
    for region in white_regions:
        # Remove if area is all white pixels
        for r, c in region:
            output_grid[r,c] = grid[r,c]

    return output_grid.tolist()