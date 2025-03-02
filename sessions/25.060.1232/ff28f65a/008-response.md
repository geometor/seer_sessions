# ff28f65a • 008 • refine_coder

---
```python
"""
1.  **Identify Red Rectangle**: Locate the largest contiguous block of red (value `2`) pixels in the input grid. "Largest" is defined by prioritizing width, then height, if widths are equal.
2.  **Output Grid Dimensions**:
    *   The output grid always has a height of 3.
    *   If the width of the red rectangle is greater than 1, the output grid's width is equal to the input grid's width minus the red rectangle's width, plus one.
     *  If the width of the red rectangle is 1, the output grid's width is 3.
3.  **Place Blue Pixel**: Replace the red rectangle with a single blue (value `1`) pixel.
    *   The blue pixel is always placed on the second row (index 1).
    *   The blue pixel's column is calculated as: the difference between the input grid's leftmost column and the red rectangle's leftmost column.
4. **Fill**: Fill all other cells in the output grid with white (value `0`).
"""

import numpy as np

def find_largest_red_rectangle(grid):
    """Finds the largest red rectangle in the grid."""
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    # Calculate bounding box for each red pixel cluster
    min_row, min_col = np.min(red_pixels, axis=0)
    max_row, max_col = np.max(red_pixels, axis=0)
    width = max_col - min_col + 1
    height = max_row - min_row + 1

    return (min_row, min_col, width, height)

def transform(input_grid):
    # Find the largest red rectangle.
    rectangle_info = find_largest_red_rectangle(input_grid)

    # Determine output grid dimensions.
    if rectangle_info:
        _, rect_left_col, rect_width, _ = rectangle_info
        if rect_width > 1:
            output_width = input_grid.shape[1] - rect_width + 1
        else:
            output_width = 3
    else:
        output_width = input_grid.shape[1]  # Should not happen in this task
    output_height = 3

    # Initialize output grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place blue pixel.
    if rectangle_info:
        _, rect_left_col, _, _ = rectangle_info
        blue_col = input_grid.shape[1] - input_grid.shape[1] + rect_left_col # simplifies to just rect_left_col
        output_grid[1, blue_col] = 1

    return output_grid
```
