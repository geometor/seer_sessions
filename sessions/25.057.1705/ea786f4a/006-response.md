# ea786f4a • 006 • refine_coder

---
```python
"""
Identifies the largest rectangle of a non-white color in the input grid and changes the color of its corner pixels to white (0).
"""

import numpy as np

def get_rectangle_info(grid):
    """
    Identifies a rectangle in the grid and returns its corner coordinates and color.
    Assumes the rectangle is the largest contiguous block of a single, non-white color.

    Args:
        grid (numpy.ndarray): grid to process

    Returns:
        tuple: corners, target_color, max_area
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
        return None, None, None

    rows, cols = np.where(grid == target_color)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    corners = [(min_row, min_col), (min_row, max_col), (max_row, min_col), (max_row, max_col)]
    return corners, target_color, max_area

def transform(input_grid):
    """
    Transforms the input grid by finding the largest rectangle of non-white color
    and setting its corner pixels to white (0).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get the corner coordinates and color of the largest rectangle
    corners, _, _ = get_rectangle_info(input_grid)

    # If a rectangle is found, change the color of its corner pixels to white (0)
    if corners:
        for row, col in corners:
            output_grid[row, col] = 0

    return output_grid
```
