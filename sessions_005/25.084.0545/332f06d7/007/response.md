```python
"""
1.  **Identify Contiguous Regions:** Divide the grid into contiguous regions.  Adjacency includes diagonals (8-way connectivity, not just 4-way). A region is a group of one or more connected pixels, regardless of their color.
2.  **Check for Blue:** For each region, determine if it contains *any* blue (1) pixels.
3.  **Conditional Transformation:**
    *   If a region contains blue:
        *   Change all white (0) pixels within that region to blue (1).
        *   Change all red (2) pixels within that region to blue (1).
    *   If a region does *not* contain blue:
        *   Leave all pixels in that region unchanged.
4.  **Green Invariance:** Never change green (3) pixels, regardless of their region.
"""

import numpy as np

def find_contiguous_regions(grid):
    """
    Finds contiguous regions in a grid using 8-way connectivity.

    Args:
        grid: The input grid (numpy array).

    Returns:
        A labeled array where each contiguous region has a unique integer label,
        and the number of regions.
    """
    rows, cols = grid.shape
    labeled_grid = np.zeros_like(grid, dtype=int)
    region_count = 0
    
    def dfs(row, col, region_label):
        if row < 0 or row >= rows or col < 0 or col >= cols or labeled_grid[row, col] != 0 or visited[row, col]:
            return
        visited[row, col] = True
        labeled_grid[row, col] = region_label
        # Explore 8-way neighbors
        for dr in [-1, -1, -1, 0, 0, 1, 1, 1]:
            for dc in [-1, 0, 1, -1, 1, -1, 0, 1]:
                dfs(row + dr, col + dc, region_label)

    visited = np.zeros_like(grid, dtype=bool)
    for r in range(rows):
        for c in range(cols):
            if labeled_grid[r, c] == 0:
                region_count += 1
                dfs(r, c, region_count)
    return labeled_grid, region_count

def region_contains_color(grid, labeled_regions, region_label, color):
    """
    Checks if a specific contiguous region contains a specified color.

    Args:
        grid: The original grid.
        labeled_regions: The labeled regions array.
        region_label: The label of the region to check.
        color: The color to check for.

    Returns:
        True if the region contains the color, False otherwise.
    """
    region_pixels = grid[labeled_regions == region_label]
    return color in region_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all contiguous regions
    labeled_regions, num_regions = find_contiguous_regions(input_grid)

    # Iterate through all regions
    for region_label in range(1, num_regions + 1):
        # Check if the region contains blue (color 1)
        if region_contains_color(input_grid, labeled_regions, region_label, 1):
            # Iterate through the pixels in the region
            for r in range(input_grid.shape[0]):
                for c in range(input_grid.shape[1]):
                    # Apply transformation rules:
                    if labeled_regions[r, c] == region_label:
                        if output_grid[r, c] == 0 or output_grid[r, c] == 2:
                            output_grid[r, c] = 1

    return output_grid
```