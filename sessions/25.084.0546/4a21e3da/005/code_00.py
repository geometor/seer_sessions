"""
Transforms an input grid by identifying orange (7) and red (2) regions, connecting them, and then filling areas with orange (7) based on symmetry around the red region(s). Blue (1) acts as a background and is replaced by orange in the filling process.
"""

import numpy as np

def get_objects(grid, color):
    """Identifies and returns a list of contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)
        dfs(r + 1, c + 1, current_object)
        dfs(r - 1, c - 1, current_object)
        dfs(r + 1, c - 1, current_object)
        dfs(r - 1, c + 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(region):
    """Calculates the bounding box of a region."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in region:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)

def get_neighbors(grid, r, c, include_diagonal=False):
    """Returns the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    if include_diagonal:
        for dr, dc in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr,nc))
    return neighbors


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.ones_like(input_grid)  # Initialize with blue (1)
    rows, cols = input_grid.shape

    # 1. Identify Key Elements
    orange_regions = get_objects(input_grid, 7)
    red_regions = get_objects(input_grid, 2)

    # 2. Combine all orange and red pixels into a single list for easier processing
    all_orange_red = []
    for region in orange_regions:
        for r, c in region:
            all_orange_red.append((r,c))
            output_grid[r,c] = 7

    for region in red_regions:
        for r,c in region:
            all_orange_red.append((r,c))
            output_grid[r,c] = 2

    # 3. Determine the "inside" region based on a bounding box and fill
    if len(all_orange_red) > 0:
        (min_r, min_c), (max_r, max_c) = get_bounding_box(all_orange_red)

        for r in range(min_r, max_r+1):
            for c in range(min_c, max_c + 1):
                output_grid[r,c] = 7  # initial fill
                if (r,c) in all_orange_red:
                    if input_grid[r,c] == 2:
                        output_grid[r,c] = 2 # put back any reds


    # 4.  Outside fill - two neighbors
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 1: # if still blue
                neighbors = get_neighbors(output_grid, r,c)
                orange_count = 0
                for nr,nc in neighbors:
                    if output_grid[nr,nc] == 7:
                        orange_count+=1
                if orange_count >= 2:
                    output_grid[r,c] = 7

    return output_grid