```python
"""
1.  **Identify Target Object:** Find the contiguous block of non-black (non-zero) pixels. It can be a vertical or horizontal line.
2.  **Determine Action:**
    *   If target object is vertical, remove the bottom row.
    *   Remove all columns not containing the target object.
    *   Remove all rows not containing the target object.
3.  **Output:** A new grid containing only the target object with potential reduced rows (vertical lines) or columns (horizontal lines.)
"""

import numpy as np

def find_object(grid):
    """Finds the bounding box of the contiguous non-zero object."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = 0, 0
    target_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                if target_color == 0:
                    target_color = grid[r, c]
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    if target_color == 0:
        return None, None

    return target_color, (min_row, min_col, max_row, max_col)


def transform(input_grid):
    """Transforms the input grid based on the object's shape and position."""

    # Find the object
    target_color, bbox = find_object(input_grid)

    if bbox is None:
        return np.zeros((1, 1), dtype=int)

    min_row, min_col, max_row, max_col = bbox

    # Determine object shape (vertical or horizontal line)
    if max_row - min_row > max_col - min_col:  # Vertical line
        # Remove the bottom row
        max_row -= 1
    
    # Extract the object using the bounding box
    output_grid = input_grid[min_row:max_row + 1, min_col:max_col + 1]

    return output_grid
```