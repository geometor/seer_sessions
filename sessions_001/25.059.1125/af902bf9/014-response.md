# af902bf9 • 014 • refine_coder

---
```python
"""
Copies yellow pixels from the input grid to the output grid and adds a red rectangle in the output grid. The red rectangle's position and size are determined by the bounding box of the gray object in the input grid.
"""

import numpy as np

def find_pixels_by_value(grid, value):
    """Finds the coordinates of pixels with a specific value."""
    return np.argwhere(grid == value).tolist()

def get_bounding_box(grid, value):
    """
    Calculates the bounding box of a set of pixels with the specified color.
    Returns (top_left, bottom_right) coordinates of the object
    """
    pixels = find_pixels_by_value(grid, value)
    if not pixels:
        return None, None  # Handle cases where no object of specified color exists
    min_row, min_col = np.min(pixels, axis=0)
    max_row, max_col = np.max(pixels, axis=0)
    return (min_row, min_col), (max_row, max_col)

def create_rectangle(grid, top_left, bottom_right, value):
    """Fills a rectangular region in the grid with a given value."""
    if top_left is None or bottom_right is None:
        return grid

    for r in range(top_left[0], bottom_right[0] + 1):
        for c in range(top_left[1], bottom_right[1] + 1):
            # Handle cases when rectangle goes outside the grid
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                grid[r, c] = value
    return grid

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find yellow pixels (value 4)
    yellow_pixels = find_pixels_by_value(input_grid, 4)

    # Preserve yellow pixels
    for pixel in yellow_pixels:
       output_grid[pixel[0], pixel[1]] = 4

    # Find the bounding box of the gray object (value 5)
    top_left, bottom_right = get_bounding_box(input_grid, 5)

    # Create red rectangle (value 2) with the same dimensions and position as gray object
    output_grid = create_rectangle(output_grid, top_left, bottom_right, 2)

    return output_grid
```
