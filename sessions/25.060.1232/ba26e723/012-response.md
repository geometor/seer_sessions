# ba26e723 • 012 • refine_coder

---
```python
"""
Identifies contiguous white regions and changes the color of yellow pixels that form the external corners of these regions to magenta.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds contiguous regions of a given color in the grid.
    Returns a list of sets, where each set contains the coordinates of a contiguous region.
    """
    visited = set()
    regions = []

    def dfs(r, c, current_region):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_region.add((r, c))
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_region = set()
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def is_external_corner(grid, r, c, white_regions):
    """
    Checks if a yellow pixel at (r, c) is an external corner of a white region.
    A corner is external if it's adjacent to a white region but doesn't encroach upon a 2x2 white square.
    """
    if grid[r,c] != 4:
        return False

    for region in white_regions:
        # Check for adjacency to the white region
        adjacent = False
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (r + dr, c + dc) in region:
                adjacent = True
                break
        if not adjacent:
            continue
        
        # Check if this encroaches a 2x2 area
        for r_start in [r - 1, r]:
            for c_start in [c-1, c]:
                if all((r_start + dr, c_start + dc) in region  for dr in range(2) for dc in range(2)):
                    return False

        return True

    return False


def transform(input_grid):
    """
    Transforms the input grid by changing yellow pixels at the external corners of white regions to magenta.
    """
    output_grid = np.copy(input_grid)
    white_regions = find_contiguous_regions(input_grid, 0)

    # Iterate through all yellow pixels and check for external corners
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if is_external_corner(output_grid, r, c, white_regions):
                output_grid[r, c] = 6

    return output_grid
```
