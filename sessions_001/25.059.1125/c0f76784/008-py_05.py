"""
1.  **Identify Gray Regions:** Locate all contiguous blocks of gray (5) pixels within the grid. These are our regions of interest.

2.  **Identify Inner Pixels:** Within each gray region, determine the "inner" pixels. An inner pixel is defined as a gray pixel that has gray pixels directly above, below, to the left, and to the right. All subsequent operations within a gray region *only* apply to these inner pixels.

3. **Azure Replacement:**
    Within each gray region, find any horizontal straight lines of 3 or more 'inner' gray pixels.
      - If the line has an odd number of pixels, change the color of the very center pixel of that line to azure (8).
      - If the line has an even number of pixels, change the color of the center *two* pixels of that line to azure (8).

4.  **Magenta Replacement:** Within each gray region, for each inner gray pixel, check if *all* the following conditions apply:
      - there is an azure pixel directly above it
      - the gray pixel is adjacent on its left, right, *and* above to *another gray pixel*.
    If all conditions are true, change the inner gray pixel's color to magenta (6).

5.  **Orange Replacement:** Within each gray region, find any 2x2 squares consisting *entirely* of inner gray pixels. If found, change the color of *all four* pixels in that 2x2 square to orange (7).

6.  **Preservation:** Any pixel not explicitly modified by the above steps retains its original color.
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

        # Horizontal Line Detection and Replacement (Azure)
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
            if (r-1, c) in np.ndindex(output_grid.shape) and output_grid[r-1, c] == 8:  # Check for azure above
                neighbors = [(r-1, c), (r, c-1), (r, c+1)] # top, left, right
                is_surrounded = True
                for nr, nc in neighbors:
                    if not (0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and output_grid[nr,nc] == 5):
                        is_surrounded = False
                        break
                if is_surrounded:
                    output_grid[r, c] = 6

        # 2x2 Square Detection and Replacement (Orange)
        for r, c in inner_pixels:
            if (r+1, c) in inner_pixels and (r, c+1) in inner_pixels and (r+1, c+1) in inner_pixels:
                output_grid[r, c] = 7
                output_grid[r+1, c] = 7
                output_grid[r, c+1] = 7
                output_grid[r+1, c+1] = 7

    return output_grid