# 890034e9 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of color 8 (azure) within the input grid.
2.  **Targeted Replacement:** within each azure region
    *   If the azure region spans 5 consecutive horizontal cells, keep it, and move to next azure region.
    *   If azure region is less than 5 consecutive horizontal cells, keep azure.
    *   If the azure region is more than 5 horizontal cells, analyze as follows:
        1.  Replace the first and last two 8s with colour of cell directly above. If there is no cell directly above (at edge of grid) maintain 8.
        2.  Within the now shortened azure region (with 2 cells at start/end removed) replace with colour directly above. If there is no cell directly above, maintain 8.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    regions = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_region):
        """Depth-first search to find contiguous region."""
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
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    azure_regions = find_contiguous_regions(input_grid, 8)

    for region in azure_regions:
        # Sort the region by column to easily check horizontal spans
        region.sort(key=lambda x: (x[0], x[1]))  # Sort by row, then by column
        
        # Group cells by row
        rows = {}
        for r, c in region:
            if r not in rows:
                rows[r] = []
            rows[r].append((r,c))

        for row, cells in rows.items():
           
            #get length of horizontal span for region on this row
            horizontal_span = len(cells)

            if horizontal_span > 5 :
              #first and last two
              for i in range (min(2, horizontal_span)):
                r, c = cells[i]
                if r > 0:
                    output_grid[r,c] = input_grid[r-1, c]

                r, c = cells[horizontal_span - 1 - i]
                if r > 0:
                    output_grid[r,c] = input_grid[r-1, c]

              #now replace intermediate cells
              for i in range (2, horizontal_span - 2):
                r, c = cells[i]
                if r > 0:
                  output_grid[r,c] = input_grid[r-1, c]

    return output_grid
```
