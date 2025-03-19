# 10fcaaa3 • 010 • refine_coder

---
```python
"""
1.  **Identify Magenta Pixels:** Locate all magenta (6) pixels in the input grid.

2.  **Duplicate Magenta Pixels:** For *each* magenta pixel in the input grid, create a duplicate magenta pixel in the output grid. The duplicate's row is the *same* as the original.  The duplicate's column is the original magenta pixel's column plus a fixed horizontal offset. The horizontal offset equals the difference between the max and min column that has a magenta pixel.

3.  **Azure Fill:** For each row where there are both original and duplicated magenta pixels:
    * find the column of the leftmost and rightmost magenta pixel (original or duplicate)
    * fill all pixels between the original and duplicated magenta pixels with azure (8), inclusive, in that row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid, same size as input
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height, input_width), dtype=int)

    # find original magenta pixels
    magenta_pixels = []
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 6:
                magenta_pixels.append((row, col))

    # calculate horizontal offset
    if magenta_pixels:
      min_col = min( [ col for _, col in magenta_pixels ] )
      max_col = max( [ col for _, col in magenta_pixels ] )
      horizontal_offset = max_col - min_col
    else:
      horizontal_offset = 0
    
    # duplicate magenta pixels and azure fill
    for row, col in magenta_pixels:
        # original magenta
        output_grid[row, col] = 6
        # duplicate magenta
        new_col = col + horizontal_offset
        if new_col < input_width:
          output_grid[row,new_col] = 6

          # azure fill between
          for fill_col in range(min(col,new_col), max(col,new_col)+1 ):
            if output_grid[row,fill_col] == 0:
              output_grid[row, fill_col] = 8

    return output_grid
```
