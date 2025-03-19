# ea786f4a • 019 • refine_coder

---
```python
"""
1. Examine Central Column: Inspect the central column of the input grid.
2. Identify Non-Gray Pixel: Locate the single pixel within this column that is *not* gray (color value 5).
3. Get Pixel Color: Note the color value of this non-gray pixel.
4. Propagate to Output: In the output grid:
    *   Set all pixels in the central row to the identified color.
    *   Set all pixels in the central column to the identified color.
5. Output initialization: Initialize a copy of input grid as the output grid.
"""

import numpy as np

def find_non_gray_pixel(grid):
    """Finds the coordinates of the non-gray pixel in the central column."""
    rows, cols = grid.shape
    center_col = cols // 2
    for row in range(rows):
        if grid[row, center_col] != 5:
            return row, center_col
    return None  # Should not happen, based on task description

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find the coordinates of non-gray pixel
    non_gray_coords = find_non_gray_pixel(input_grid)

    # Check if non_gray_coords exist and handle the case where they don't.
    if non_gray_coords is not None:
      center_row, center_col = non_gray_coords
    else:
       return output_grid # Return original if not found for some unexpected reason.

    # get center pixel color
    center_color = input_grid[center_row, center_col]

    # find center row index
    output_center_row = rows // 2
    
    # change output pixels 
    for i in range(rows):
        output_grid[i, center_col] = center_color  # change pixels on central column
    for j in range(cols):
        output_grid[output_center_row, j] = center_color  # change pixels on central row
    
    return output_grid
```
