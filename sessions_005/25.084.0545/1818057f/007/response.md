```python
"""
1.  **Identify Regions:** Find all contiguous regions of red (2) pixels and yellow (4) pixels.

2.  **Iterative Transformation:** For each yellow region:
    *   If the yellow region contains more than one pixel:
        *   Iterate until no more changes occur:
            *   Change any yellow pixel within the region to azure (8) if it is adjacent (horizontally or vertically) to either a red (2) pixel *or* an azure (8) pixel.
"""

import numpy as np
from scipy.ndimage import label

def get_adjacent_pixels(grid, row, col):
    # helper to get adjacent pixel coords
    rows, cols = grid.shape
    adjacent_pixels = []
    if row > 0:
        adjacent_pixels.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))  # Down
    if col > 0:
        adjacent_pixels.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))  # Right
    return adjacent_pixels

def is_adjacent_to_red_or_azure(grid, row, col):
    # helper to check for adjacent red or azure pixels
    for r, c in get_adjacent_pixels(grid, row, col):
        if grid[r, c] == 2 or grid[r, c] == 8:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find yellow regions
    yellow_pixels = (input_grid == 4)
    labeled_yellow, num_yellow_regions = label(yellow_pixels)

    # Iterate through each yellow region
    for region_id in range(1, num_yellow_regions + 1):
        region_mask = (labeled_yellow == region_id)
        region_size = np.sum(region_mask)

        # Check if region size is greater than 1
        if region_size > 1:
            # Iterative transformation
            changes_made = True
            while changes_made:
                changes_made = False
                for row in range(rows):
                    for col in range(cols):
                        if region_mask[row, col] and output_grid[row, col] == 4 and is_adjacent_to_red_or_azure(output_grid, row, col):
                            output_grid[row, col] = 8
                            changes_made = True

    return output_grid
```
