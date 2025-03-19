# e40b9e2f • 008 • refine_coder

---
```python
"""
1. **Identify the Object:** Determine the bounding box of the contiguous non-background pixels. This defines the "primary shape".
2. **Color Swap:** Within the bounding box, exchange all yellow (4) pixels with orange (7) pixels, and vice versa.
3. **Reflect and Position**: Reflect the shape. The reflection rule appears to perform these steps:
    - swap colors
    - flip the object along both axes. It may require multiple flips or may be better
described as a 180 degree rotation.
    - move the reflected shape to a new position on the grid. The new position will either be
      - along the same row
      - along the same column
      - centered along the vertical and horizontal axis relative to the
        original position.
"""

import numpy as np

def get_shape_bounds(grid):
    """Finds the bounding box of the non-zero pixels."""
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

def rotate_180(shape):
    """Rotates the shape 180 degrees."""
    return np.rot90(shape, 2)

def calculate_new_position(input_bounds, rotated_shape, input_grid):
    """Calculates the new position for the reflected shape."""
    min_row, max_row, min_col, max_col = input_bounds
    input_center_row = (min_row + max_row) // 2
    input_center_col = (min_col + max_col) // 2

    output_rows, output_cols = rotated_shape.shape
    
    # Check for horizontal or vertical movement.
    # prioritize horizontal, then veritical, then diagonal.
    
    # horizontal
    if np.any(input_grid[input_center_row,:] != 0):
        new_min_col = input_grid.shape[1] - output_cols - min_col
        new_min_row = min_row
        if new_min_col < 0: # doesn't work, lets try vertical
           new_min_col = min_col
           new_min_row = input_grid.shape[0] - output_rows - min_row     
    
    #vertical
    elif np.any(input_grid[:,input_center_col] != 0):
        new_min_row = input_grid.shape[0] - output_rows - min_row
        new_min_col = min_col
    # default to diagonal centering if no clear horizontal or vertical.
    else:
        new_min_row = input_grid.shape[0] -  output_rows - min_row
        new_min_col = input_grid.shape[1] - output_cols - min_col
        

    return new_min_row, new_min_col


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the Object
    input_bounds = get_shape_bounds(input_grid)
    if input_bounds is None:
        return output_grid

    min_row, max_row, min_col, max_col = input_bounds
    shape = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 2. Color Swap
    swapped_shape = swap_colors(shape)

    # 3. Reflect and Position
    rotated_shape = rotate_180(swapped_shape)
    new_min_row, new_min_col = calculate_new_position(input_bounds, rotated_shape, input_grid)

    # Place the transformed shape back into the output grid.
    output_rows, output_cols = rotated_shape.shape

    # Handle cases where the new position might be out of bounds. Clip.
    new_max_row = min(new_min_row + output_rows, output_grid.shape[0])
    new_max_col = min(new_min_col + output_cols, output_grid.shape[1])
    
    output_grid[new_min_row:new_max_row, new_min_col:new_max_col] = rotated_shape[:new_max_row-new_min_row,:new_max_col-new_min_col] # clip in case of out-of-bounds

    return output_grid
```
