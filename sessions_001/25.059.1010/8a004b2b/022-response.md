# 8a004b2b • 022 • refine_coder

---
```python
"""
1.  **Identify Regions:** Locate all contiguous regions of non-zero colored pixels and single non-zero pixels within the input grid.
2.  **Fill Rows:** For each row in the grid, find the right-most non-zero pixel. Fill all pixels to the left of this pixel with the same color.
3.  **Reposition Yellow Pixels:** Find all single pixels of color 4 (yellow). Move these pixels to the corners of the grid. The corners are filled in this order: top-left, top-right, bottom-left, bottom-right. If there are more yellow pixels than corners, leave the extra yellow pixels in place. If a corner is not background, move to the next corner.
"""

import numpy as np

def find_regions(grid):
    """Finds contiguous regions of non-zero colors and single non-zero pixels."""
    regions = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, region_type):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return []

        visited.add((r, c))
        region = [(r, c)]

        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            region.extend(dfs(nr, nc, color, region_type))
        return region

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                region = dfs(r, c, color, 'block' if any(grid[nr, nc] == color for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)] if is_valid(nr,nc)) else 'single')
                if(region):
                    regions.append({'color': color, 'pixels': region, 'type': 'block' if len(region) > 1 else 'single'})
    return regions

def fill_rows(grid):
    """Fills each row with the right-most non-zero color."""
    output_grid = np.copy(grid)
    rows, cols = output_grid.shape
    for r in range(rows):
        rightmost_color = 0
        for c in range(cols - 1, -1, -1):
            if output_grid[r, c] != 0:
                rightmost_color = output_grid[r, c]
            elif rightmost_color != 0:
                output_grid[r, c] = rightmost_color
    return output_grid

def reposition_yellow_pixels(grid, regions):
    """Moves yellow (4) pixels to the corners of the grid."""
    output_grid = np.copy(grid)
    yellow_pixels = [region['pixels'][0] for region in regions if region['color'] == 4 and region['type'] == 'single']
    rows, cols = output_grid.shape
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]

    yellow_idx = 0
    for cr, cc in corners:
        if yellow_idx < len(yellow_pixels) and output_grid[cr,cc] == 0:
            # Remove yellow pixel from its current position
            output_grid[yellow_pixels[yellow_idx][0], yellow_pixels[yellow_idx][1]] = 0
            # Place in new corner
            output_grid[cr, cc] = 4
            yellow_idx += 1

    return output_grid


def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)

    # 1. Find Regions
    regions = find_regions(output_grid)

    # 2. Fill Rows
    output_grid = fill_rows(output_grid)
    
    # Need to find regions again after filling
    regions = find_regions(output_grid)

    # 3. Reposition Yellow Pixels
    output_grid = reposition_yellow_pixels(output_grid, regions)

    return output_grid
```

