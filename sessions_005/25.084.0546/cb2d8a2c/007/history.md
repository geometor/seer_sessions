
Previous Code:
```python
"""
1.  **Convert Blue to Red:** Replace all blue (1) pixels with red (2) pixels.
2.  **Identify Isolated Red Regions:** Before any expansion, identify connected regions of red (2) pixels. A red region is considered "isolated" if none of its pixels are directly adjacent (horizontally, vertically, *or diagonally*) to a green (3) pixel.
3.  **Expand Existing Green Regions Conditionally:** For each existing green (3) pixel, check for adjacent red (2) pixels (horizontally or vertically).
    *   If a red pixel is found adjacent to the green:
        *   Expand the green region vertically upwards from the green pixel, stopping if a background (8) pixel or the edge of the grid is encountered.
        *   Expand the green region vertically downwards from the green pixel, stopping if a background (8) pixel or the edge of the grid is encountered.
4.  **Insert Green to the Left of Isolated Red Regions:** For each *isolated* red region (determined in step 2):
    * Find the top row of each isolated red region.
    *   Insert green (3) pixels to the left of the entire isolated region, starting at the top row and filling all columns to the left of the leftmost red pixel in the region.
5.  **Expand the Inserted Green Vertically:** Extend the newly inserted green pixels (from step 4) vertically (up and down).
    *  Expand upwards, stopping at a background (8) pixel, existing green (3) pixel, or the grid edge.
    *  Expand downwards, stopping at a background (8) pixel, existing green (3) pixel, or the grid edge.
6.  **Preserve Background:** Ensure all background (8) pixels that were not part of any transformation remain unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c, include_diagonal=False):
    """Get the neighbors of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (i != 0 and j != 0):
              continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def get_connected_regions(grid, value, include_diagonal=False):
    """Find connected regions of a specific value."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(r, c, current_region):
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or visited[r, c]
            or grid[r, c] != value
        ):
            return
        visited[r, c] = True
        current_region.append((r, c))
        for nr, nc in get_neighbors(grid, r, c, include_diagonal):
            dfs(nr, nc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                regions.append(current_region)
    return regions

def is_isolated(region, grid):
    """Checks if a region is isolated (not adjacent to green)."""
    for r, c in region:
        for nr, nc in get_neighbors(grid, r, c, include_diagonal=True):
            if grid[nr, nc] == 3:
                return False  # Found an adjacent green pixel
    return True

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Convert Blue to Red
    output_grid[output_grid == 1] = 2

    # 2. Identify Isolated Red Regions (before expansion)
    red_regions = get_connected_regions(output_grid, 2)
    isolated_red_regions = [region for region in red_regions if is_isolated(region, output_grid)]

    # 3. Expand Existing Green Regions Conditionally
    existing_greens = np.argwhere(output_grid == 3)
    for r, c in existing_greens:
        neighbors = get_neighbors(output_grid, r, c)  # Only orthogonal
        for nr, nc in neighbors:
            if output_grid[nr, nc] == 2:
                # Expand vertically upwards
                ur = r - 1
                while ur >= 0 and output_grid[ur, nc] != 8:
                    output_grid[ur, nc] = 3
                    ur -= 1
                # Expand vertically downwards
                dr = r + 1
                while dr < rows and output_grid[dr, nc] != 8:
                    output_grid[dr, nc] = 3
                    dr += 1

    # 4. Insert Green to the Left of Isolated Red Regions
    for region in isolated_red_regions:
        min_row = min(r for r, c in region)
        min_col = min(c for r, c in region)
        for c in range(min_col):
          output_grid[min_row,c] = 3

    # 5. Expand the Inserted Green Vertically
    for region in isolated_red_regions:
        min_row = min(r for r, c in region)
        min_col = min(c for r, c in region)

        # expand up
        ur = min_row - 1
        while ur >= 0 and output_grid[ur, min_col -1] != 8:
          for c in range(min_col):
            if output_grid[ur,c] != 3:
              output_grid[ur,c] = 3
          ur -= 1
        # expand down
        dr = min_row + 1
        while dr < rows and output_grid[dr, min_col-1] != 8:
          for c in range(min_col):
            if output_grid[dr,c] != 3:
              output_grid[dr,c] = 3
          dr += 1

    # 6. Preserve Background (Implicit in the logic)
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 2 1 2 1 2 1
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8
8 3 3 3 3 3 3 3 3 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 2 2 2 2 2 2 2
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 29
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 23.481781376518228

## Example 2:
Input:
```
8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
3 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8
```
Expected Output:
```
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 8 2 8 8 8 8 8 3 3 3 3 3 3 3
8 8 8 8 3 8 2 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 3 8 2 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 3 8 2 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 3 8 8 8 8 8 8 8 3 8 8 8 2 8 8
8 8 8 8 3 3 3 3 3 3 3 3 3 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
```
Transformed Output:
```
3 3 3 3 3 3 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
3 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8
```
Match: False
Pixels Off: 46
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.482972136222912

## Example 3:
Input:
```
8 8 8 8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 1 2 1
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 2 1 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 2 8 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 8 8 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.05263157894737

## Example 4:
Input:
```
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
3 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 8 8 2 8 8 8 8 8 8 3 3 3 3 3 3 3
8 8 3 8 8 2 8 8 8 8 8 8 3 8 8 8 8 8 8
8 8 3 8 8 8 8 8 8 8 8 8 3 8 2 8 8 8 8
8 8 3 8 8 8 8 8 8 8 8 8 3 8 2 8 8 8 8
8 8 3 3 3 3 3 3 3 3 3 3 3 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
```
Transformed Output:
```
3 3 3 3 3 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
3 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 3 3 3 3 3 3 3 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
```
Match: False
Pixels Off: 41
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 35.96491228070175
Okay, let's analyze the results of the previous code execution and strategize improvements.

**General Assessment:**

The code performs some of the intended transformations, but it fails to correctly handle the spatial relationships and conditional expansions, especially concerning the interaction between green and red pixels. The vertical expansion of green is overly aggressive and not properly constrained by the presence of background pixels or other green pixels. The insertion of green to the left of isolated red regions is also not completely accurate, sometimes stopping too soon. The diagonal adjacency check seems correct but not the orthogonal adjacency, as the inserted greens don't correctly expand vertically.

**Strategy for Resolving Errors:**

1.  **Refine Green Expansion:** The vertical expansion of green needs to be more carefully controlled. It should stop not only at background (8) pixels but also at existing green (3) pixels. Moreover, the expansion seems to happen regardless of direct adjacency to a red pixel *after* the initial blue-to-red conversion. The logic should consider the adjacency *after* the conversion and not only based on initial green positions.

2.  **Correct Left-Side Green Insertion:** The placement of green to the left of isolated red regions needs adjustment. It seems the logic doesn't correctly extend up/down on all examples, sometimes it does not start in the correct row, or it extends too far.

3.  **Re-evaluate Adjacency:** Ensure that the adjacency checks (horizontal, vertical, and diagonal) are correctly used in the appropriate contexts. The conditional expansion of existing green pixels needs to consider adjacency *after* step 1 (blue-to-red conversion).

4. Improve structure of steps 4. and 5. by correctly filling and expanding in the proper order.

**Metrics Gathering (using code execution when needed):**

I'll manually go over each example here, since I've already seen the visual outputs. A code execution block isn't strictly necessary for this manual comparison.

*   **Example 1:** The expansion of the single green pixel is incorrect. It expands too far downwards and misses some upwards expansion. Green insertion to the left of the red is correct in placement, but expansion is missing.
*   **Example 2:** Conditional expansion due to existing green pixels does not account for the transformed red. Green insertion misses multiple blocks. The vertical expansion of the inserted Green is overly aggressive.
*   **Example 3:** Similar problems to example 2: existing green expansion occurs everywhere; inserted green is not expanded correctly.
*   **Example 4:** Similar errors, especially with the conditional expansion of existing green and the inserted green expansion missing rows.

**YAML Fact Documentation:**


```yaml
facts:
  - task: "Conditional Green Expansion and Insertion"
  - objects:
    - type: pixel
      properties:
        color:
          - white (0)
          - blue (1)
          - red (2)
          - green (3)
          - azure (8)
      actions:
        - change_color:
            from: blue
            to: red
        - expand_conditionally:
            color: green
            condition: "adjacent to red (horizontally or vertically)"
            direction: vertical
            stop_conditions: [background, green]
        - insert:
            color: green
            condition: "left of isolated red regions"
            reference: "top row of region"
        - expand_inserted:
          color: green
          direction: up/down
          condition: all columns to the left of region
          stop_conditions: [ background, green ]
  - relationships:
    - adjacency:
        types: [horizontal, vertical, diagonal]
    - isolation:
        condition: "red region not adjacent to green (including diagonally)"
```


**Natural Language Program:**

1.  **Convert Blue to Red:** Change all blue pixels to red.
2.  **Identify Isolated Red Regions:** Find all connected regions of red pixels. A region is isolated if none of its pixels are adjacent (horizontally, vertically, or diagonally) to a green pixel.
3.  **Conditional Green Expansion:** For *each* green pixel in the grid *after* step 1, if it's adjacent (horizontally or vertically) to a red pixel, extend the green vertically (both up and down). Stop the expansion when encountering a background pixel or another green pixel.
4.  **Insert Green to the Left of Isolated Red:** For each isolated red region, find the top row and the leftmost column of the region. Insert green pixels in all columns to the left of the region's leftmost column, starting from the top row of the region.
5. **Expand Inserted Green**: Expand the green inserted (from step 4).
    * From the top row of the isolated red region to the top of the grid.
    * From the bottom row of the isolated red region to the bottom of the grid.
    Stopping expansion at background (8) or other green (3) pixels.


