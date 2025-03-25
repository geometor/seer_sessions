```python
"""
1.  **Identify Regions:** Identify all contiguous regions of orange (7) pixels and red (2) pixels.  A region consists of pixels of the same color connected horizontally or vertically.
2.  **Determine Relative Position and Adjacency:** Determine the relative positions of the orange and red regions based on a top-to-bottom, left-to-right reading order. For each orange region, check if it *is* adjacent to any red region.
3.  **Transform Orange Regions:**
    *   If an orange region *is* adjacent to any red region, change *all* pixels in the orange region to green (3).
    *   If an orange region is *not* adjacent to any red region (based on top-bottom, left-right positioning), change *all* pixels in that orange region to gray (5).
4.  **Preserve Red Regions:** Red (2) pixels are unchanged.
"""

import numpy as np
from scipy.ndimage import label

def get_regions(grid, color):
    """
    Identifies contiguous regions of a specific color in the grid.
    """
    colored_grid = (grid == color).astype(int)
    labeled_grid, num_labels = label(colored_grid)
    regions = []
    for i in range(1, num_labels + 1):
        regions.append(np.where(labeled_grid == i))
    return regions

def is_adjacent(region, other_color_regions, grid):
    """
    Checks if a given region is adjacent to any region of another color.
    """
    rows, cols = region
    for r, c in zip(rows, cols):
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))  # Up
        if r < grid.shape[0] - 1:
            neighbors.append((r + 1, c))  # Down
        if c > 0:
            neighbors.append((r, c - 1))  # Left
        if c < grid.shape[1] - 1:
            neighbors.append((r, c + 1))  # Right

        for neighbor_row, neighbor_col in neighbors:
            for other_region in other_color_regions:
                other_rows, other_cols = other_region
                if (neighbor_row, neighbor_col) in zip(other_rows, other_cols):
                    return True
    return False

def get_top_left(region):
    """Returns the top-left coordinate of a region."""
    rows, cols = region
    min_row_index = np.argmin(rows)
    min_col_index = np.argmin(cols)

    #if multiple with the same min row, use the one with the lowest col.
    min_row = rows[min_row_index]
    min_cols_at_min_row = cols[rows == min_row]
    min_col = np.min(min_cols_at_min_row)

    return min_row, min_col

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # 1. Identify Regions
    orange_regions = get_regions(input_grid, 7)
    red_regions = get_regions(input_grid, 2)

    # 2 & 3. Transform Orange Regions based on Adjacency and Position
    for orange_region in orange_regions:
        adjacent_to_red = is_adjacent(orange_region, red_regions, input_grid)
        
        if not adjacent_to_red:
            output_grid[orange_region] = 5 # Change to gray
            continue

        # check position - any red must be "before" orange
        orange_top_left = get_top_left(orange_region)
        is_before = False
        for red_region in red_regions:
          red_top_left = get_top_left(red_region)
          if (red_top_left[0] < orange_top_left[0] or
              (red_top_left[0] == orange_top_left[0] and red_top_left[1] < orange_top_left[1])):
            is_before = True
            break

        if adjacent_to_red:
            output_grid[orange_region] = 3  # Change to green

    return output_grid
```