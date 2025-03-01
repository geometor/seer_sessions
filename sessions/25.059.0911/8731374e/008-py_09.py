"""
1. Examine the input grid: Check for the presence of blue (1) pixels.
2. Handle No Blue Pixels: If there are no blue pixels in the input, the output is a 3x1 grid filled entirely with blue (1).
3. If Blue Pixels Exist:
    *   Find the largest connected region of blue pixels.
    *   The output grid's height is the same as the height of input grid.
    *   The output grid's width is 6.
4. Checkerboard Pattern: Create a checkerboard pattern using blue (1) and red (2) in the output grid, the checkerboard always starts with color red at the top-left position (0,0)
"""

import numpy as np

def find_largest_connected_region(grid, color):
    """Finds the largest connected region of a given color in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    max_region = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, col, current_region)
        dfs(row, col - 1, col, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                if len(current_region) > len(max_region):
                    max_region = current_region
    return max_region

def transform(input_grid):
    # Check for the presence of blue pixels.
    blue_region = find_largest_connected_region(input_grid, 1)

    # Handle no blue pixels case.
    if not blue_region:
        return np.array([[1], [1], [1]])

    # Determine output grid dimensions.
    output_height = input_grid.shape[0]
    output_width = 6

    # Create the output grid with a checkerboard pattern.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for row in range(output_height):
        for col in range(output_width):
            # Checkerboard starts with red (2) at (0, 0).
            if (row + col) % 2 == 0:
                output_grid[row, col] = 2  # Red
            else:
                output_grid[row, col] = 1  # Blue

    return output_grid