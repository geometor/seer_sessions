"""
1.  **Initialize Output:** Create an output grid of the same dimensions as the input grid, filled with black (0).
2.  **Identify Green Regions:** Locate all contiguous regions of green (3) pixels in the input grid.
3.  **Combine Green Regions:** Create a single rectangular green region that encompasses all identified green regions using a bounding box. Fill this bounding box with green (3) in the output grid.
4.  **Identify and Replace Yellow Pixels:** Find isolated yellow (4) pixels in the input grid. Replace these with gray (5) pixels in the output grid.
5.  **Identify the cluster:** Find the cluster of pixels containing yellow(4), gray(5), and magenta(6).
6.  **Integrate Cluster:** Place the cluster of pixels in the output grid retaining shape and position.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all contiguous objects of a given color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def find_single_pixels(grid, color):
    """Finds isolated pixels of the specified color."""
    pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == color:
                pixels.append((r,c))
    return pixels

def get_cluster(grid):
    """Get cluster of gray(5), magenta(6) and yellow(4)"""
    cluster_pixels = {}
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row,col] in [5,6,4]:
                cluster_pixels[(row,col)] = grid[row,col]

    return cluster_pixels

def get_bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return (0, 0, 0, 0)
    min_row = min(r for r, _ in pixels)
    max_row = max(r for r, _ in pixels)
    min_col = min(c for _, c in pixels)
    max_col = max(c for _, c in pixels)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full_like(input_grid, 0)

    # Find objects
    green_regions = find_objects(input_grid, 3)
    yellow_pixels = find_single_pixels(input_grid, 4)
    cluster = get_cluster(input_grid)

    # Combine green regions using a bounding box
    combined_green = []
    for region in green_regions:
        combined_green.extend(region)
    min_r, max_r, min_c, max_c = get_bounding_box(combined_green)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            output_grid[r, c] = 3

    # Replace yellow pixels
    for r, c in yellow_pixels:
        output_grid[r,c] = 5 # Replace yellow with gray

    # Integrate Cluster
    for (r, c), color in cluster.items():
        output_grid[r,c] = color

    return output_grid