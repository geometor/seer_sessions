"""
Identifies distinct colored regions in the input grid, preserves their original colors, and reconstructs an output grid preserving the relative positions and shapes of these regions. The output grid's size is determined dynamically based on the maximum row and column indices of *all* pixels within the regions.
"""

import numpy as np

def find_regions(grid):
    """Finds all distinct connected regions (objects) in the grid."""
    regions = {}
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, region_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        region_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, region_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore white
                    region_coords = []
                    dfs(r, c, color, region_coords)
                    # Use top-left as key
                    min_r = min(coord[0] for coord in region_coords)
                    min_c = min(coord[1] for coord in region_coords)
                    regions[(min_r, min_c)] = (color, region_coords)
    return regions

def determine_output_size(regions):
    """Determines the output grid size based on *all* region pixel positions."""
    if not regions:
        return 0, 0

    max_r = 0
    max_c = 0
    for _, (_, region_coords) in regions.items():
        for r, c in region_coords:
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    return max_r + 1, max_c + 1

def transform(input_grid):
    """Transforms the input grid according to the ARC task rules."""
    # Find regions in the input grid
    regions = find_regions(np.array(input_grid))

    # Determine output size dynamically, based on ALL pixels in ALL regions
    output_rows, output_cols = determine_output_size(regions)
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Reconstruct the output grid, iterating through ALL pixels of each region
    for (start_r, start_c), (color, region_coords) in regions.items():
        for r, c in region_coords:
            output_grid[r, c] = color  # Place pixel at its absolute position

    return output_grid