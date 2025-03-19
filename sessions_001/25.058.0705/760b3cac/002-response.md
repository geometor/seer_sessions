# 760b3cac • 002 • example_1 • investigate_coder

---
```python
"""
The transformation selectively shifts azure pixels to the left within their respective rows, filling the closest empty (white, 0) space to their left, while keeping other colored pixels unchanged.
"""

import numpy as np

def get_object_locations(grid, color):
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    azure_pixels = get_object_locations(input_grid, 8)

    for row in range(rows):
        row_azure_pixels = azure_pixels[azure_pixels[:, 0] == row]

        if len(row_azure_pixels) == 0: # skip row if no azure pixels in this row
            continue

        # find white spaces in the row
        row_white_pixels = np.where(input_grid[row] == 0)[0]
        
        # shift azure pixels
        for azure_pixel in row_azure_pixels:
           
           white_pixels_left = row_white_pixels[row_white_pixels < azure_pixel[1]]
           
           if len(white_pixels_left)>0:
              leftmost_white = np.max(white_pixels_left)
              output_grid[row, azure_pixel[1]] = 0
              output_grid[row, leftmost_white] = 8
           

    return output_grid
```
