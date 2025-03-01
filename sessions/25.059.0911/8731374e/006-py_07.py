"""
The program identifies the largest connected region of blue (1) pixels in the input grid. 
If no blue pixels are present, a 1x1 blue grid is returned. Otherwise, it creates a checkerboard 
pattern of blue (1) and red (2) pixels in a new grid. The output grid's width is always 6 if any
blue is present, and height is 5 if the blue region height is > 1, otherwise height is 3.
The checkerboard pattern starts with blue at the top-left corner of the bounding box of the
input blue region.
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
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                if len(current_region) > len(max_region):
                    max_region = current_region
    return max_region

def transform(input_grid):
    # Find the largest connected region of blue (1) pixels.
    blue_region = find_largest_connected_region(input_grid, 1)

    if not blue_region:
        return np.array([[1]]) # handle edge case with no blue.

    # Determine the bounding box of the blue region.
    min_row = min(r for r, c in blue_region)
    max_row = max(r for r, c in blue_region)
    min_col = min(c for r, c in blue_region)
    max_col = max(c for r, c in blue_region)

    # Determine output grid dimensions.
    output_width = 6
    output_height = 5 if (max_row - min_row + 1) > 1 else 3

    # Create the output grid with a checkerboard pattern.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for row in range(output_height):
        for col in range(output_width):
            # Calculate checkerboard pattern based on the top-left of the blue region.
            if (row + col - min_row - min_col) % 2 == 0:
                 # Offset by min_row and min_col to align checkerboard
                output_grid[row, col] = 1  # Blue
            else:
                output_grid[row, col] = 2  # Red

    return output_grid