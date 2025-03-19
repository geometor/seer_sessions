# e40b9e2f • 006 • refine_coder

---
```python
"""
1. Identify the primary shape: Find the bounding box containing all non-background (non-zero) pixels. This defines the object.
2. Swap Colors: Within the bounding box, change all yellow (4) pixels to orange (7) and all orange (7) pixels to yellow (4).
3. Reflect/Rotate: The shape is reflected.
    - If the shape is a square, reflect along both horizontal and vertical axis (which is equivalent to 180 degree rotation).
    - If the shape is a horizontal rectangle, reflect along the vertical axis.
    - If the shape is a vertical rectangle, reflect along the horizontal axis.
    - This can be implemented as a series of reflections, or a rotation.
"""

import numpy as np

def get_shape_bounds(grid):
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def swap_colors(shape):
    """Swaps yellow (4) and orange (7) pixels within a shape."""
    new_shape = np.copy(shape)
    new_shape[shape == 4] = 77  # Temporary value
    new_shape[shape == 7] = 4
    new_shape[new_shape == 77] = 7
    return new_shape

def reflect_shape(shape):
    """Reflects the shape based on its dimensions."""
    rows, cols = shape.shape
    if rows == cols:  # Square
        return np.flipud(np.fliplr(shape)) # reflect both axes
    elif cols > rows:  # Horizontal rectangle
        return np.fliplr(shape) # reflect vertical
    else:  # Vertical rectangle
        return np.flipud(shape) # reflect horizontal

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the primary shape
    bounds = get_shape_bounds(input_grid)
    if bounds is None:
        return output_grid

    min_row, max_row, min_col, max_col = bounds
    shape = input_grid[min_row:max_row+1, min_col:max_col+1]
    
    # 2. Swap Colors
    swapped_shape = swap_colors(shape)

    # 3. Reflect/Rotate
    reflected_shape = reflect_shape(swapped_shape)

    # Place the transformed shape back into the output grid.
    output_grid[min_row:max_row+1, min_col:max_col+1] = reflected_shape
    
    return output_grid
```
