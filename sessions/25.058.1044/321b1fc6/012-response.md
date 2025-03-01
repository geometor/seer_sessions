# 321b1fc6 • 012 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure (8) pixels in the input grid.
2. **Check for existing color on same rows:**
    * If any row that contains part of an azure region ALSO contains an orange (7) pixel, change all pixels in that azure region to orange (7).
    * If any row that contains part of an azure region ALSO contains a magenta (6) pixel, change all pixels in that azure region to magenta (6).
3.  **Determine New Color (if no orange/magenta on same row):** For each azure region *not yet changed*, determine the starting row index of the region.
    *   If the starting row index is less than 4, change all pixels in that region to orange (7).
    *   Otherwise, change all pixels in that region to magenta (6).
4.  **Output:** Return the modified grid.
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore a region."""
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

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find all azure (8) regions
    azure_regions = find_regions(input_grid, 8)

    # Iterate through each azure region
    for region in azure_regions:
        rows = [r for r, _ in region]
        
        # Check for orange (7) or magenta (6) on the same rows
        change_to_orange = False
        change_to_magenta = False

        for row in rows:
            if 7 in input_grid[row, :]:
                change_to_orange = True
                break
            if 6 in input_grid[row, :]:
                change_to_magenta = True
                break

        if change_to_orange:
            for row, col in region:
                output_grid[row, col] = 7
        elif change_to_magenta:
            for row, col in region:
                output_grid[row, col] = 6
        else:
            # Determine color based on first row if not changed by existing colors
            first_row = region[0][0]
            if first_row < 4:
                new_color = 7
            else:
                new_color = 6
            for row, col in region:
                output_grid[row, col] = new_color


    return output_grid
```

