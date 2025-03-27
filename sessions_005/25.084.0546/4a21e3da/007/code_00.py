"""
Transforms an input grid by identifying orange (7) and red (2) regions, then filling areas with orange (7) based on a reflection/mirroring operation around the red region(s). Blue (1) background pixels are replaced by orange in the filling process, while original orange and red pixels remain.
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
        dfs(r + 1, c + 1, current_object)  # Diagonal
        dfs(r - 1, c - 1, current_object)  # Diagonal
        dfs(r + 1, c - 1, current_object)  # Diagonal
        dfs(r - 1, c + 1, current_object)  # Diagonal


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def get_centroid(region):
    """Calculates the centroid of a region."""
    if not region:
        return None
    sum_r = sum(r for r, c in region)
    sum_c = sum(c for r, c in region)
    return (sum_r / len(region), sum_c / len(region))

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    output_grid = np.copy(input_grid)  # Start with a copy
    rows, cols = input_grid.shape

    # 1. Identify Key Elements
    orange_regions = get_objects(input_grid, 7)
    red_regions = get_objects(input_grid, 2)

    # 2.  Handle the reflection/mirroring.
    if red_regions and orange_regions: # only reflect if we have both
        for red_region in red_regions:
            red_centroid = get_centroid(red_region)

            for orange_region in orange_regions:
              for orange_r, orange_c in orange_region:
                # Calculate reflected position
                diff_r = orange_r - red_centroid[0]
                diff_c = orange_c - red_centroid[1]
                
                # integer arithmetic
                reflected_r = int(red_centroid[0] - diff_r)
                reflected_c = int(red_centroid[1] - diff_c)

                # Check bounds and fill
                if 0 <= reflected_r < rows and 0 <= reflected_c < cols:
                  output_grid[reflected_r, reflected_c] = 7  # Fill reflected pixel

    # original orange and red stay the same
    for region in orange_regions:
        for r, c in region:
            output_grid[r,c] = 7

    for region in red_regions:
        for r,c in region:
            output_grid[r,c] = 2 # put back any reds

    return output_grid