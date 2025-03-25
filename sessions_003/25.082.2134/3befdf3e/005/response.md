```python
"""
1.  **Identify the Central Object:** Find the smallest rectangular region (bounding box) in the input grid that contains all non-background (non-zero) pixels. This defines the "central object."

2.  **Determine Border and Inner Colors:**
    *   The "border color" is the color of the pixel at the top-left corner of the central object's bounding box.
    *   If the central object has a width and height greater than 2, the "inner color" is the color of the pixel one step inward from the top-left corner of the bounding box.
    *   Otherwise, if the width or height is 2 or less, the "inner color" is the same as the "border color."

3.  **Expand the Bounding Box:** Increase the size of the bounding box by one pixel in all four directions (up, down, left, right). This creates a new, larger rectangle. The dimensions increase by two in each direction (height + 2, width + 2).

4.  **Fill the Expanded Region:**
    *   All cells that fall *within* the expanded bounding box, but were *outside* the original bounding box, are filled with the border color.
    *   All cells that fall *within* the expanded bounding box, and are *not* part of the border, are filled with the inner color.

5.  **Preserve Unchanged Pixels:** All pixels outside the expanded bounding box remain unchanged from their original values in the input grid.
6.  If there are no objects, return the original input grid unchanged.
"""

import numpy as np

def find_central_object(grid):
    # Find the bounding box of the non-zero pixels
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid
        return None, None, None, None, None, None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)

    # Get border and inner colors
    border_color = grid[min_row, min_col]
    if (max_row - min_row + 1) > 2 and (max_col - min_col + 1) > 2:
        inner_color = grid[min_row + 1, min_col + 1]
    else:
        inner_color = border_color

    return min_row, max_row, min_col, max_col, border_color, inner_color

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.array(input_grid).copy()

    # Find the central object
    min_row, max_row, min_col, max_col, border_color, inner_color = find_central_object(output_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid

    # Calculate expanded dimensions
    new_min_row = max(0, min_row - 1)
    new_max_row = min(output_grid.shape[0] - 1, max_row + 1)
    new_min_col = max(0, min_col - 1)
    new_max_col = min(output_grid.shape[1] - 1, max_col + 1)

    # Fill the expanded region with the inner color
    output_grid[new_min_row:new_max_row+1, new_min_col:new_max_col+1] = inner_color

    # Apply border color to the new border (expanded region)
    output_grid[new_min_row:new_max_row+1, new_min_col] = border_color  # Left border
    output_grid[new_min_row:new_max_row+1, new_max_col] = border_color  # Right border
    output_grid[new_min_row, new_min_col:new_max_col+1] = border_color  # Top border
    output_grid[new_max_row, new_min_col:new_max_col+1] = border_color  # Bottom border
    
    return output_grid
```