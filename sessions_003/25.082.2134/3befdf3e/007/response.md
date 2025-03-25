```python
"""
1.  **Identify the Central Object:** Find the smallest rectangle (bounding box) encompassing all non-zero (colored) pixels in the input grid.

2.  **Determine Border and Inner Colors:**
    *   The border color is the color of the pixel in the top-left corner of the central object's bounding box.
    *   If the central object has a width and height greater than 2, the inner color is the color of the pixel one step diagonally inward from the top-left corner of the bounding box.
    *   If the central object's width or height is 2 or less, the inner color is the same as the border color.

3.  **Expand Bounding Box:** Expand the bounding box by one pixel in all directions (up, down, left, and right).

4.  **Fill Border:** Fill the newly added border region (the pixels that are part of the expanded bounding box but *not* the original bounding box) with the border color.

5.  **Fill Inside:** Fill the remaining pixels *within* the expanded bounding box (excluding the border created in step 4) with the inner color.

6.  **Preserve Background:** Pixels outside the expanded bounding box are unchanged.
7.  If there are no objects (no non-zero pixels), return the original input.
"""

import numpy as np

def find_central_object(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None, None, None, None, None, None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)

    border_color = grid[min_row, min_col]
    if (max_row - min_row + 1) > 2 and (max_col - min_col + 1) > 2:
        inner_color = grid[min_row + 1, min_col + 1]
    else:
        inner_color = border_color

    return min_row, max_row, min_col, max_col, border_color, inner_color

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.array(input_grid).copy()

    # Find the central object and its properties
    min_row, max_row, min_col, max_col, border_color, inner_color = find_central_object(output_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid

    # Calculate expanded bounding box dimensions
    new_min_row = max(0, min_row - 1)
    new_max_row = min(output_grid.shape[0] - 1, max_row + 1)
    new_min_col = max(0, min_col - 1)
    new_max_col = min(output_grid.shape[1] - 1, max_col + 1)

    # Fill the expanded border
    # Top border
    output_grid[new_min_row, new_min_col:new_max_col+1] = border_color
    # Bottom border
    output_grid[new_max_row, new_min_col:new_max_col+1] = border_color
    # Left border
    output_grid[new_min_row:new_max_row+1, new_min_col] = border_color
    # Right border
    output_grid[new_min_row:new_max_row+1, new_max_col] = border_color

    # Fill the inner region
    output_grid[new_min_row+1:new_max_row, new_min_col+1:new_max_col] = inner_color

    return output_grid
```