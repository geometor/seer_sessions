# 928ad970 • 022 • refine_coder

---
```python
"""
1.  **Identify Objects:** Locate all *isolated* pixels of gray (5), yellow (4), and green (3). An isolated pixel is one that has no adjacent pixels (horizontally, vertically, or diagonally) of the same color. Also locate contiguous regions of yellow (4).

2.  **Preserve Isolated Pixels:** The positions and colors of the isolated pixels remain unchanged in the output grid.

3.  **Expand Contiguous Yellow Region (if present):** If a contiguous region (more than one pixel) of yellow exists, expand it outward in all eight directions (including diagonals) one layer at time.

    *   The expansion stops when it encounters either an isolated pixel of *any* color, or an edge of the grid.
    *   The yellow pixels expand one layer at a time.

4.  **Output:** The resulting grid, with preserved isolated pixels and the potentially expanded yellow region, is the transformation.
"""

import numpy as np

def find_isolated_pixels(grid, colors):
    """
    Find isolated pixels of specified colors in the grid.
    """
    isolated = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] in colors:
                is_isolated = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                            if grid[nr, nc] == grid[r, c]:
                                is_isolated = False
                                break
                    if not is_isolated:
                        break
                if is_isolated:
                    isolated.append((r, c))
    return isolated

def find_yellow_regions(grid):
    """
    Find contiguous regions of yellow (4).
    """
    regions = []
    visited = set()

    def dfs(r, c, current_region):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != 4:
            return
        visited.add((r, c))
        current_region.append((r, c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 4 and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                if len(current_region) > 1:  # Only consider regions with more than one pixel
                    regions.append(current_region)
    return regions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find isolated pixels (gray, yellow, green)
    isolated_pixels = find_isolated_pixels(input_grid, [5, 4, 3])

    # find yellow regions
    yellow_regions = find_yellow_regions(input_grid)

    # expand yellow region
    if yellow_regions:
        for region in yellow_regions:
            expanded_region = set(region)
            while True:
                new_expanded_region = set(expanded_region)
                for r, c in expanded_region:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1] and
                                    input_grid[nr, nc] == 0 and (nr, nc) not in isolated_pixels):
                                #expand to white and not to isolated pixels
                                new_expanded_region.add((nr, nc))
                if new_expanded_region == expanded_region:
                  break
                else:
                  expanded_region = new_expanded_region

            for r,c in expanded_region:
              output_grid[r,c] = 4

    # preserve isolated pixels
    for r, c in isolated_pixels:
        output_grid[r, c] = input_grid[r, c]  # Use original color

    return output_grid
```
