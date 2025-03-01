# e509e548 • 014 • refine_coder

---
```python
"""
1.  **Identify Green Regions:** Find all distinct, contiguous regions of green (3) pixels in the input grid.  Orthogonal connectivity (up, down, left, right) defines contiguity.

2.  **Categorize Region Position:**  For each green region, determine its position category using these rules:
    *   **Top-Left:** If the region's minimum row is within the top half of the grid *and* its minimum column is within the left half of the grid, recolor to blue (1).
    *   **Bottom-Left:** If the region's minimum row is within the bottom half of the grid *and* its minimum column is within the left half of the grid, recolor to red (2).
    *   **Top-Right:** If the region's minimum row is within the top half of the grid *and* its maximum column is within the right half of the grid, recolor to magenta (6).

3.  **Recolor:** Change all pixels within each green region to the color determined by its category.

4.  **Output:** The output grid consists of the original grid with the recolored green regions. All other colors in original input should be the same in the output.
"""

import numpy as np

def find_connected_regions(grid, color):
    # Find all connected regions of a specific color
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def get_region_position_category(region, grid_shape):
    # Determine the position category of a region
    min_row = min(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)

    grid_height, grid_width = grid_shape
    center_row = (grid_height - 1) / 2
    center_col = (grid_width - 1) / 2

    # Top-Left: min_row in top half, min_col in left half
    if min_row <= center_row and min_col <= center_col:
        return "top-left"
    # Bottom-Left: min_row in bottom half, min_col in left half
    if min_row > center_row and min_col <= center_col:
        return "bottom-left"
    # Top-Right: min_row in top half, max_col in right half
    if min_row <= center_row and max_col > center_col:
        return "top-right"

    return "other"  # Should not be used, based on the task description

def transform(input_grid):
    # Initialize output grid with the same values as the input
    output_grid = input_grid.copy()

    # Find connected regions of green (color 3)
    green_regions = find_connected_regions(input_grid, 3)

    # Recolor each region based on its position category
    for region in green_regions:
        position_category = get_region_position_category(region, input_grid.shape)

        if position_category == "top-left":
            new_color = 1  # Blue
        elif position_category == "bottom-left":
            new_color = 2  # Red
        elif position_category == "top-right":
            new_color = 6  # Magenta
        else:
            new_color = 0 # Black - should not happen

        for row, col in region:
            output_grid[row, col] = new_color

    return output_grid
```
