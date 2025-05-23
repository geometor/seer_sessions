# a64e4611 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Blue Shapes:** Locate all disconnected shapes formed by blue (1) pixels in the input grid.
2.  **Determine Bounding Rectangle:** Find the smallest rectangular region within the grid that completely encloses all identified blue shapes. This rectangle's boundaries are defined by the minimum and maximum row and column indices of all blue pixels.
3.  **Replace with Green:** In the output grid, keep all the original blue cells from input. Replace all white (0) pixels *within* the bounding rectangle (identified in step 2) with green (3) pixels. Leave all other pixels (those outside the bounding rectangle) unchanged from the input grid. This means white pixels outside the rectangle, stay white.
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
    
       # Replace with Green
       for i in range(min_row, max_row + 1):
           for j in range(min_col, max_col + 1):
              if output_grid[i,j] == 0:
                output_grid[i, j] = 3
    return output_grid
```
