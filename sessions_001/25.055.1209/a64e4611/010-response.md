# a64e4611 • 010 • refine_coder

---
```python
"""
1.  **Identify Blue Pixels:** Locate all pixels with the color blue (value 1) in the input grid.
2.  **Determine Bounding Rectangle:** Calculate the smallest rectangular region that encloses all identified blue pixels. This rectangle is defined by the minimum and maximum row and column indices of the blue pixels.
3.  **Transform Non-Blue Pixels:** Within the bounding rectangle, change the color of *every* pixel that is *not* blue (1) to green (3).
4. **Preserve Input:** Pixels outside of the bounding box are not changed.
"""

import numpy as np

def get_bounding_box(grid):
    """Find the bounding box of blue pixels."""
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
        return None  # Handle case with no blue pixels

    min_row = blue_pixels[:, 0].min()
    max_row = blue_pixels[:, 0].max()
    min_col = blue_pixels[:, 1].min()
    max_col = blue_pixels[:, 1].max()

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    
    output_grid = np.copy(input_grid)
    
    # Determine Bounding Rectangle
    bounding_box = get_bounding_box(input_grid)

    if bounding_box:
       min_row, max_row, min_col, max_col = bounding_box
    
       # Transform Non-Blue Pixels
       for i in range(min_row, max_row + 1):
           for j in range(min_col, max_col + 1):
              if output_grid[i,j] != 1: # Check if NOT blue
                output_grid[i, j] = 3
    return output_grid
```

