"""
1.  **Identify the Background:** Determine the most frequent color in the input grid. This is the background color.

2.  **Select Sub-region:** In the lower half of the input grid, find the smallest rectangular region (bounding box) that contains all pixels that are *not* the background color.

3.  **Mirror Sub-region:** Create a vertically flipped (mirrored) copy of the selected sub-region.

4.  **Overlay Mirrored Region:** Overlay the mirrored sub-region onto the *top* of the output grid. The top edge of the mirrored sub-region should align with the top edge of the output grid. The left and right edges of the mirrored subregion should align with the `min_col` and `max_col` that were determined when selecting the original sub-region. The height is determined by the size of the mirrored sub-region.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Finds the most frequent color in a grid."""
    color_counts = Counter(grid.flatten())
    return color_counts.most_common(1)[0][0]

def select_subregion(grid, background_color):
    """Finds the bounding box of non-background pixels in the lower half."""
    rows, cols = grid.shape
    min_row, max_row = rows, 0
    min_col, max_col = cols, 0

    for r in range(rows // 2, rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)
    return min_row, max_row, min_col, max_col

def mirror_subregion(grid, min_row, max_row, min_col, max_col):
    """Vertically flips the selected sub-region."""
    subregion = grid[min_row:max_row+1, min_col:max_col+1]
    return np.flipud(subregion)

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Identify the background color
    background_color = get_background_color(input_grid)

    # Select the sub-region in the lower half
    min_row, max_row, min_col, max_col = select_subregion(input_grid, background_color)

    # Create a mirrored copy of the sub-region
    mirrored_region = mirror_subregion(input_grid, min_row, max_row, min_col, max_col)

    # Overlay the mirrored region onto the top of the output grid
    rows_mirrored = mirrored_region.shape[0]
    output_grid[0:rows_mirrored, min_col:max_col+1] = mirrored_region

    return output_grid.tolist()