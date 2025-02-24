# a85d4709 • 006 • refine_coder

---
```python
"""
The transformation replaces 0s (white pixels) adjacent to 5s (gray pixels) in the input grid with 2s, 3s, or 4s based on their relative position to the gray region, following a clockwise color pattern starting from the top.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to find contiguous pixels."""
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

def get_replacement_color(gray_region, zero_pos):
    """Determines the replacement color for a zero based on its position relative to the gray region."""
    zero_row, zero_col = zero_pos

    # Find min and max row/col of gray region
    min_gray_row = min(pos[0] for pos in gray_region)
    max_gray_row = max(pos[0] for pos in gray_region)
    min_gray_col = min(pos[1] for pos in gray_region)
    max_gray_col = max(pos[1] for pos in gray_region)
    
    if zero_row < min_gray_row:
        return 4  # Above
    elif zero_row > max_gray_row:
        return 2  # Below
    elif zero_col < min_gray_col:
        return 4 # Left
    elif zero_col > max_gray_col:
        return 3 # Right

    return 0 # Should not reach here, as 0s should always be adjacent

def is_adjacent(zero_pos, gray_region):
    """Checks if a zero position is adjacent to any pixel in the gray region."""
    zero_row, zero_col = zero_pos
    for gray_row, gray_col in gray_region:
        if (
            abs(zero_row - gray_row) <= 1
            and abs(zero_col - gray_col) <= 1
            and (zero_row != gray_row or zero_col != gray_col)  # Not the same pixel
        ):
            return True
    return False

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = input_grid.copy()

    # Find contiguous regions of 0s and 5s
    zero_regions = find_contiguous_regions(input_grid, 0)
    five_regions = find_contiguous_regions(input_grid, 5)

    # Iterate through each zero region
    for zero_region in zero_regions:
        # Iterate through five regions
        for five_region in five_regions:
          for zero_pos in zero_region:
              if is_adjacent(zero_pos, five_region):
                replacement_color = get_replacement_color(five_region, zero_pos)
                output_grid[zero_pos] = replacement_color
    return output_grid
```
