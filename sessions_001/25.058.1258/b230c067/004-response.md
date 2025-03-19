# b230c067 • 004 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels in the input grid.  A contiguous region is a group of connected pixels of the same color, where connectivity is defined by the 4 cardinal directions (up, down, left, right).

2.  **Determine Replacement Color:** For each identified azure region, determine the replacement color based on these rules:

    *   **Red (2):** If the region contains ANY pixels existing in the last 3
        rows AND last 3 columns, the replacement color is red.
    *   **Blue (1):** All other azure regions are replaced with blue.

3.  **Apply Replacement:** Replace the azure pixels in each region with their determined replacement color.

4.  **Preserve Background:** Keep all white (0) pixels unchanged (they are the background and do not participate in the transformation).
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """
    Finds all contiguous regions of a specified color in a grid.

    Args:
        grid: A 2D numpy array representing the grid.
        color: The color to find regions of.

    Returns:
        A list of lists, where each inner list contains (row, col) tuples
        representing a contiguous region of the specified color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
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
    output_grid = np.copy(input_grid)

    # Find all azure regions
    azure_regions = find_contiguous_regions(input_grid, 8)

    # Determine replacement color and apply
    for region in azure_regions:
        replace_color = 1  # Default to blue

        # Check if any part of the region is in the last 3 rows and cols
        max_row = input_grid.shape[0]
        max_col = input_grid.shape[1]
        for row, col in region:
            if row >= max_row - 3 and col >= max_col - 3:
                replace_color = 2
                break  # Once we find a red case, no need to check further

        for row, col in region:
            output_grid[row, col] = replace_color

    return output_grid
```
