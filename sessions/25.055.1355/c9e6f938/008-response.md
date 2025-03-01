# c9e6f938 • 008 • example_2 • investigate_coder

---
```python
"""
Identifies a contiguous block of orange (7) pixels in the input grid and expands it horizontally, doubling its width. White (0) pixels remain unchanged.
"""

import numpy as np

def find_orange_shape(grid):
    # Find coordinates of orange pixels
    orange_pixels = np.argwhere(grid == 7)
    if orange_pixels.size == 0:
        return None, None, None

    # Determine bounding box of the shape
    min_row, min_col = np.min(orange_pixels, axis=0)
    max_row, max_col = np.max(orange_pixels, axis=0)
    return (min_row, min_col), (max_row, max_col), orange_pixels

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the orange shape
    top_left, bottom_right, orange_pixels = find_orange_shape(input_grid)

    # Initialize output grid with white pixels
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

   # If no orange pixels, we return array with doubled width
    if top_left is None:
        return output_grid
    
    # Calculate original width
    original_width = bottom_right[1] - top_left[1] + 1
    
    # calculate expansion amount
    expansion_amount = original_width
    
    # Copy original orange
    for row, col in orange_pixels:
        new_col = col
        output_grid[row, new_col] = 7

    # Copy expanded shape
    for row, col in orange_pixels:
        new_col = col + expansion_amount
        output_grid[row, new_col] = 7    

    return output_grid
```
