"""
1. **Analyze Input Grid:** Scan the input grid to identify distinct rectangular regions. A region is defined as a contiguous block of pixels sharing the same color, and bounded by pixels of color 0 (white) or the edge of the grid.

2. **Extract Representative Colors:** For each identified region, record the color value (0-9) of that region.

3.  **Construct Output Grid:** create the output grid with dimensions 2xN, where N the number of distinct pairs of colors, with the pairs separated by blank/white (0) lines in the input grid.

4.  **Position Colors:** for each pair of regions identified in step 1, one is placed above the other in order of their discovery, and colored using the representative color identified in Step 2.
"""

import numpy as np

def find_regions(grid):
    """
    Identifies distinct rectangular regions of uniform color in the input grid.
    """
    regions = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, region_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        region_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, region_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                region_coords = []
                dfs(r, c, grid[r, c], region_coords)
                if region_coords:
                    min_r = min(coord[0] for coord in region_coords)
                    max_r = max(coord[0] for coord in region_coords)
                    min_c = min(coord[1] for coord in region_coords)
                    max_c = max(coord[1] for coord in region_coords)

                    regions.append({
                        'color': grid[r, c],
                        'min_row': min_r,
                        'max_row': max_r,
                        'min_col': min_c,
                        'max_col': max_c
                    })
    return regions

def transform(input_grid):
    # Find regions in the input grid
    regions = find_regions(np.array(input_grid))
    
    # Calculate output grid size 
    num_pairs = len(regions)
    output_height = 2
    output_width = (num_pairs + 1) // 2 #integer division

    # Initialize the output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill the output grid with colors from the regions
    
    for i, region in enumerate(regions):
      output_grid[i%2,i//2] = region['color']

    return output_grid.tolist()