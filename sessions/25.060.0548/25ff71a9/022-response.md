# 25ff71a9 • 022 • refine_coder

---
```python
"""
The input grid contains a connected shape formed by blue pixels. This shape is rotated 90 degrees clockwise. The output grid's dimensions are determined by the rotated shape, and the shape is placed in the top-left corner of the output grid. The rest of the output grid is filled with white pixels.
"""

import numpy as np

def rotate_clockwise(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def get_blue_shape(grid):
    """Extracts the connected blue shape from the grid."""
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return np.array([[]])  # Return an empty grid
    min_row = np.min(blue_pixels[:, 0])
    max_row = np.max(blue_pixels[:, 0])
    min_col = np.min(blue_pixels[:, 1])
    max_col = np.max(blue_pixels[:, 1])
    return grid[min_row:max_row+1, min_col:max_col+1]

def transform(input_grid):
    # Extract the blue shape
    blue_shape = get_blue_shape(input_grid)

    # Rotate the blue shape
    rotated_shape = rotate_clockwise(blue_shape)

    # Create a new output grid filled with white, with dimensions of the rotated shape
    output_grid = np.zeros(rotated_shape.shape, dtype=input_grid.dtype)

    # Place the rotated shape in the top-left corner
    output_grid[:rotated_shape.shape[0], :rotated_shape.shape[1]] = rotated_shape

    return output_grid
```
