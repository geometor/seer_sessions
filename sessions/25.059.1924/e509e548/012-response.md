# e509e548 • 012 • refine_coder

---
```python
"""
1.  **Find Green Regions:** Identify all distinct, contiguous regions of green (3) pixels in the input grid.  Contiguous regions are defined by orthogonally connected pixels (up, down, left, right).

2.  **Categorize Region Position:** Determine the position category of each green region based on these rules.
    *   **Top-Left:** if all pixels have coordinates where the sum of the x and y coordinates are lesser or equal to the other regions.
    *   **Bottom-Left:** If the region's minimum row is within the bottom half of the grid *and* its minimum column is within the left half of the grid.
    *   **Top-Right:** If the region's minimum row is within the top half of the grid *and* its maximum column is within the right half of the grid.
    * "Other": default

3.  **Recolor Based on Category:**  Recolor the pixels within each green region according to its position category:
    *   **Top-Left:** Change all pixels in the region to blue (1).
    *   **Bottom-Left:** Change all pixels in the region to red (2).
    *   **Top-Right:** Change all pixels in the region to magenta (6).
    *   **Other:** Do not change colors and they should be black(0)

4. **Preserve White:** Ensure all white pixels remain white.
5.  **Output:** The output grid is the result of applying these recoloring rules to the input grid.
"""

import numpy as np

def find_connected_regions(grid, color):
    # Find all connected regions of a specific color in the grid
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        # Depth-first search to find connected components
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
    max_row = max(r[0] for r in region)
    min_col = min(r[1] for r in region)
    max_col = max(r[1] for r in region)

    grid_height, grid_width = grid_shape

    # Calculate the center row and column
    center_row = (grid_height-1) / 2
    center_col = (grid_width-1) / 2
    
    # Top-Left: if all pixels have coordinates where the sum of the x and y 
    # coordinates are lesser or equal to the other regions.
    if min_row == 0 and min_col == 0:
      return "top-left"

    # Bottom-Left: If the region's minimum row is within the bottom half of the
    # grid and its minimum column is within the left half of the grid.
    if min_row >= center_row and min_col <= center_col:
        return "bottom-left"
    # Top-Right: If the region's minimum row is within the top half of the
    # grid and its maximum column is within the right half of the grid.
    if min_row <= center_row and max_col >= center_col:
        return "top-right"

    return "other"

def transform(input_grid):
    # Initialize output grid with the same dimensions and keep original colors
    output_grid = input_grid.copy()

    # Find connected regions of green (color 3)
    green_regions = find_connected_regions(input_grid, 3)

    # Recolor each region based on its position category
    for region in green_regions:
        position_category = get_region_position_category(region, input_grid.shape)

        if position_category == "top-left":
            new_color = 1
        elif position_category == "bottom-left":
            new_color = 2
        elif position_category == "top-right":
            new_color = 6
        else:
            new_color = 0 # should not happen

        for row, col in region:
            output_grid[row, col] = new_color

    return output_grid
```
