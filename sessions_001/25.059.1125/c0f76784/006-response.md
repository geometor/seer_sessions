# c0f76784 • 006 • refine_coder

---
```python
"""
1.  **Identify Gray Regions:** Find all contiguous blocks of gray (5) pixels.
2.  **Identify Inner Pixels:**  For each gray region, find the "inner" pixels. An inner pixel is a gray pixel where all four immediate neighbors (up, down, left, right) are also gray.
3.  **Horizontal Line Detection and Replacement:** Within each gray region, if there's a horizontal line of *at least* three inner gray pixels, replace the *middle* pixel(s) of that line with azure (8). If the line has an odd number of pixels, replace the single middle pixel. If the line has an even number, replace the two center-most pixels.
4.  **Magenta Replacement Below Azure:** Immediately below *any* azure pixel created in step 3, if there is an inner gray pixel and it's surrounded on its top, left, and right sides by gray, replace it with magenta (6).
5.  **2x2 Square Detection and Replacement:** Within each gray region, if there's a 2x2 square of inner gray pixels, replace all four pixels in that square with orange (7).
6.  **Preserve Other Pixels:**  All other pixels remain unchanged.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore contiguous regions."""
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
            if not visited[row, col] and grid[row, col] == color:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def find_inner_pixels(region, grid):
    """Identifies 'inner' pixels within a region."""
    inner_pixels = []
    for row, col in region:
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        is_inner = True
        for n_row, n_col in neighbors:
            if not (0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1] and grid[n_row,n_col] == 5):
                is_inner = False
                break
        if is_inner:
            inner_pixels.append((row, col))
    return inner_pixels

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    gray_regions = find_contiguous_regions(input_grid, 5)

    for region in gray_regions:
        inner_pixels = find_inner_pixels(region, input_grid)

        # Horizontal Line Detection and Replacement
        rows = {}
        for r, c in inner_pixels:
            if r not in rows:
                rows[r] = []
            rows[r].append((r, c))

        for row_num, pixels in rows.items():
            pixels.sort(key=lambda x: x[1])  # Sort by column
            line_length = 1
            for i in range(len(pixels) - 1):
                if pixels[i+1][1] == pixels[i][1] + 1:
                    line_length += 1
                else:
                    if line_length >= 3:
                        if line_length % 2 == 1:  # Odd length
                            middle_index = i - line_length // 2
                            output_grid[pixels[middle_index]] = 8
                        else:  # Even length
                            middle_index1 = i - line_length // 2
                            middle_index2 = i - line_length // 2 + 1
                            output_grid[pixels[middle_index1]] = 8
                            output_grid[pixels[middle_index2]] = 8
                    line_length = 1
            # Check for the last line segment in the row
            if line_length >= 3:
                if line_length % 2 == 1:
                    middle_index = len(pixels) - 1 - line_length // 2
                    output_grid[pixels[middle_index]] = 8
                else:
                    middle_index1 = len(pixels) - 1 - line_length // 2
                    middle_index2 = len(pixels) - 1 - line_length // 2 + 1
                    output_grid[pixels[middle_index1]] = 8
                    output_grid[pixels[middle_index2]] = 8


        # Magenta Replacement
        for r, c in inner_pixels:
            if (r-1, c) in np.ndindex(output_grid.shape) and output_grid[r-1, c] == 8:
                neighbors = [(r, c-1), (r, c+1), (r-1, c)]
                is_surrounded = True
                for nr, nc in neighbors:
                    if not (0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and output_grid[nr,nc] == 5):
                        is_surrounded = False
                        break
                if is_surrounded:
                    output_grid[r, c] = 6

        # 2x2 Square Detection and Replacement
        for r, c in inner_pixels:
            if (r+1, c) in inner_pixels and (r, c+1) in inner_pixels and (r+1, c+1) in inner_pixels:
                output_grid[r, c] = 7
                output_grid[r+1, c] = 7
                output_grid[r, c+1] = 7
                output_grid[r+1, c+1] = 7

    return output_grid
```
