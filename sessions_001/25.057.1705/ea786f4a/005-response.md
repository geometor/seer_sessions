# ea786f4a • 005 • refine_coder

---
```python
"""
1. Identify the Rectangle: Find the largest rectangular region within the input grid that consists of a single, non-white color.
2. Locate Corners: Determine the coordinates of the four corners of this rectangle: top-left, top-right, bottom-left, and bottom-right.
3. Modify Corners: In the output grid, set the color of the top-left and bottom-right corners of the rectangle to white (0).
4. Preserve other pixels. All other cells in the rectangle, and all other pixels of the input grid, keep the same color in the output grid.
"""

import numpy as np

def get_rectangle_info(grid):
    """
    Identifies a rectangle in the grid and returns its corner coordinates and color.
    Assumes the rectangle is the largest contiguous block of a single, non-white color.
    """
    colors = np.unique(grid)
    colors = colors[colors != 0]  # Exclude white (background)
    max_area = 0
    target_color = None

    for color in colors:
        rows, cols = np.where(grid == color)
        if len(rows) > 0:
            min_row, max_row = np.min(rows), np.max(rows)
            min_col, max_col = np.min(cols), np.max(cols)
            area = (max_row - min_row + 1) * (max_col - min_col + 1)
            if area > max_area:
                max_area = area
                target_color = color

    if target_color is None:
        return None, None  # No non-white rectangle found

    rows, cols = np.where(grid == target_color)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    corners = [(min_row, min_col), (min_row, max_col), (max_row, min_col), (max_row, max_col)]
    return corners, target_color

def transform(input_grid):
    """
    Transforms the input grid by setting the top-left and bottom-right corners of the largest
    non-white rectangle to white (0).
    """
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)

    # Get the corners and color of the largest rectangle.
    corners, color = get_rectangle_info(input_grid)

    # If a rectangle is found, modify the specified corners.
    if corners:
        top_left = corners[0]
        bottom_right = corners[3]
        output_grid[top_left[0], top_left[1]] = 0  # Set top-left corner to white
        output_grid[bottom_right[0], bottom_right[1]] = 0  # Set bottom-right corner to white

    return output_grid
```
