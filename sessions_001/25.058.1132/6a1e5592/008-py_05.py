"""
Replaces gray pixels with white and conditionally replaces white pixels enclosed by red pixels with blue.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_inside_outline(pixel, outline_pixels, grid_shape):
    """
    Checks if a pixel is inside a contiguous outline using a ray-casting approach.
    A pixel is enclosed if rays cast in all four orthogonal directions intersect
    with the outline.
    """
    row, col = pixel
    
    # Check if the pixel itself is part of the outline
    if (row, col) in outline_pixels:
        return False

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    for dr, dc in directions:
        found_intersection = False
        r, c = row + dr, col + dc
        while 0 <= r < grid_shape[0] and 0 <= c < grid_shape[1]:
            if (r, c) in outline_pixels:
                found_intersection = True
                break
            r += dr
            c += dc
        if not found_intersection:
            return False  # Not enclosed in this direction

    return True  # Enclosed in all directions


def transform(input_grid):
    # Create a copy of the input grid
    output_grid = np.copy(input_grid)

    # Replace all gray (5) pixels with white (0)
    output_grid[output_grid == 5] = 0
    
    # Find contiguous regions of red pixels
    red_regions = find_contiguous_regions(output_grid, 2)
    
    red_outline_pixels = set()
    for region in red_regions:
        red_outline_pixels.update(region)

    # Find white pixels inside red outline
    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == 0:  # if it is a white pixel
                if is_inside_outline((row,col), red_outline_pixels, output_grid.shape):
                    output_grid[row, col] = 1  # set to blue
    
    return output_grid