# e73095fd • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Gray Regions:** Scan the input grid and identify all contiguous regions of gray (5) pixels. A contiguous region is defined as a group of gray pixels that are directly adjacent (not diagonal).

2.  **Shape Analysis:** Analyze the shape of each gray region. Differentiate between "line-like" regions (thin, elongated) and "blob-like" regions (compact, potentially enclosed).

3. **Conditional Filling**:
    *    If a gray region is classified as a "blob," meaning a closed or nearly-closed shape that contains no white cells on it's interior, replace all the gray (5) pixels *within that region* with yellow (4) pixels.

4.  **Output:** The output grid is identical to the input grid, except for the gray regions that have been filled with yellow according to the rule above.
    Line like segments of grey pixels should not be changed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (not out of bounds)."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            neighbors.append((new_row, new_col))
    return neighbors

def find_gray_regions(grid):
    """Finds contiguous regions of gray pixels."""
    gray_regions = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_region):
        """Depth-first search to find contiguous gray pixels."""
        visited.add((row, col))
        current_region.append((row, col))
        for r, c in get_neighbors(grid, row, col):
            if (r, c) not in visited and grid[r, c] == 5:
                dfs(r, c, current_region)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 5 and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                gray_regions.append(current_region)
    return gray_regions

def is_blob_like(grid, region):
    """Checks if a gray region is blob-like (compact, not line-like).
    
    A simple heuristic: Check if the region is enclosed or not.
    A region is considered closed if it's completely surrounded by non-gray pixels.
    """
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1
    
    # Find bounding box of the region
    for r, c in region:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # Check if all neighbors of the region are not gray (i.e., 0)
    for r, c in region:
        for nr, nc in get_neighbors(grid, r, c):
            if grid[nr, nc] == 5 and (nr, nc) not in region: #neighbor grey and outside
                return False #not enclosed.
    return True

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid)  # Initialize output grid

    # 1. Identify Gray Regions
    gray_regions = find_gray_regions(grid)

    # 2. & 3. Shape Analysis and Conditional Filling
    for region in gray_regions:
        if is_blob_like(grid, region):
            for row, col in region:
                output_grid[row, col] = 4  # Fill with yellow

    return output_grid.tolist()
```
