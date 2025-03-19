# f8a8fe49 • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions of red (color 2) and gray (color 5) pixels. Each of these regions is an individual object.
2. **Iterate and Position for Each Red Object** For each red region:
    *   Find the topmost and bottommost row indices of the *current* red region.
    *   Find all Gray regions.
    *   For each gray region:
        * Create two copies of the gray region
        * **Above:** Place one copy of the gray region such that the bottom row of the gray copy aligns with the top row of the *current* red region, and the original column positions of all pixels within the copied region are kept.
        * **Below:** Place the second copy of the gray region such that the top row of the gray region copy aligns with the bottom row of the *current* red region, preserving the original column positions.
3.  **Output:** The output grid consists of the repositioned gray regions, and the red regions in their original locations, against a black (color 0) background.
"""

import numpy as np

def find_regions(grid, color):
    """
    Finds all distinct regions of a specific color in the grid.

    Args:
        grid: The input numpy array.
        color: The color to search for.

    Returns:
        A list of regions, where each region is a list of (row, col) coordinates.
    """
    visited = set()
    regions = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_region):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_region.append((r, c))

        # Explore adjacent cells (4-connectivity)
        dfs(r + 1, c, current_region)
        dfs(r - 1, c, current_region)
        dfs(r, c + 1, current_region)
        dfs(r, c - 1, current_region)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)

    return regions

def get_row_extents(region):
    """Calculates the minimum and maximum row indices for a single region."""
    if not region:
        return 0, -1  # Handle empty region case

    min_row = float('inf')
    max_row = float('-inf')

    for r, _ in region:
        min_row = min(min_row, r)
        max_row = max(max_row, r)

    return min_row, max_row

def transform(input_grid):
    """
    Transforms the input grid by repositioning gray regions relative to each red region.
    """
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # 1. Identify Red and Gray Regions
    red_regions = find_regions(grid, 2)
    gray_regions = find_regions(grid, 5)

    # 2. Iterate through Red Regions and Position Gray Copies
    for red_region in red_regions:
        red_min_row, red_max_row = get_row_extents(red_region)

        for gray_region in gray_regions:
            gray_min_row, gray_max_row = get_row_extents(gray_region)
            gray_height = gray_max_row - gray_min_row + 1

            # Place copy above
            for r, c in gray_region:
                new_row = red_min_row - (gray_max_row - r + 1)  #Align bottom of gray to top of red
                if 0 <= new_row < output_grid.shape[0]: # boundary check
                     output_grid[new_row, c] = 5

            # Place copy below
            for r, c in gray_region:
                new_row = red_max_row + (r - gray_min_row + 1) # align top of gray to bottom of red
                if 0 <= new_row < output_grid.shape[0]: # boundary check
                    output_grid[new_row, c] = 5

    # 3. Add Red Regions (in their original positions)
    for red_region in red_regions:
        for r, c in red_region:
            output_grid[r, c] = 2

    return output_grid.tolist()
```
