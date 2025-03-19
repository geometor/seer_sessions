"""
The input is a 3x3 grid. Within the grid, identify contiguous regions of the same color as distinct objects.
Count the number of azure (8) colored objects. Azure color pixels are on the diagonals. If white pixels break the contiguity
of azure pixels in their row or column, then count each azure set of pixels as individual object.
The output is the number of these identified objects presented in red color.
"""

import numpy as np

def count_objects(grid, color):
    # Count the number of distinct objects of a specified color in the grid.
    visited = np.zeros_like(grid, dtype=bool)
    count = 0

    def is_valid(r, c):
        # check bounds
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c):
        # traverse the grid
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        # Check neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                dfs(r, c)
                count += 1
    return count

def transform(input_grid):
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Count azure objects
    azure_objects_count = count_objects(grid, 8)
    
    # Create output (scalar represented as 1x1 grid)
    output_grid = np.array([[azure_objects_count]])
    
    return output_grid