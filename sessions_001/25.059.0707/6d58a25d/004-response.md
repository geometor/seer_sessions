# 6d58a25d • 004 • example_1 • investigate_coder

---
```python
"""
The transformation identifies the maroon (9) shape and the existing azure (8) pixels. It maintains
the azure pixel positions, adds azure pixels within the bounding box of the maroon shape, and extends
a vertical line of azure pixels downwards from the bottom edge of the maroon shape's bounding box.
"""

import numpy as np

def find_bounding_box(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle the case where the color is not found
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    #find existing azure pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # Find the bounding box of the maroon shape.
    maroon_bbox = find_bounding_box(input_grid, 9)

    if maroon_bbox:  # Check if a maroon shape was actually found
        (min_row, min_col), (max_row, max_col) = maroon_bbox

        # Fill azure within the bounding box.
        output_grid[min_row:max_row+1, min_col:max_col+1] = np.where(output_grid[min_row:max_row+1, min_col:max_col+1] == 0, 8, output_grid[min_row:max_row+1, min_col:max_col+1])
        

        # Extend a vertical line of azure downwards.
        output_grid[max_row + 1:, min_col:max_col+1] = np.where(output_grid[max_row + 1:, min_col:max_col+1] == 0, 8,  output_grid[max_row + 1:, min_col:max_col+1])

    #make sure azure pixels in original grid are preserved
    for row, col in azure_pixels:
      output_grid[row,col] = 8
    return output_grid
```
