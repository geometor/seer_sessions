# 3bd67248 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Gray Pixels:** Locate all pixels in the input grid that are gray (value 5). These are the "anchor" or "source" pixels for the transformation.

2.  **Conditional White Pixel Replacement:** Iterate through the white (value 0) pixels in the input grid.
  * if a white pixel is at the top right corner, replace with red.
  * if a white pixel is below a gray pixel AND to the right of a gray pixel, replace with yellow
  * if a white pixel is to the right of a gray AND above a yellow, replace with red.
  * if a white pixel is under a gray AND to the left of a yellow, replace with red.

3.  **Preserve Gray Pixels:** The gray pixels from the input grid remain unchanged in the output grid.
"""

import numpy as np

def get_gray_pixels(grid):
    # find coordinates of gray pixels
    gray_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 5:
                gray_pixels.append((i, j))
    return gray_pixels

def transform(input_grid):
    output_grid = np.copy(input_grid)
    gray_pixels = get_gray_pixels(input_grid)

    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 0:  # White pixel
                # Top-right corner
                if i == 0 and j == 2:
                    output_grid[i,j] = 2
                
                is_below_gray = False
                is_right_of_gray = False
                is_right_of_gray_above_yellow = False
                is_under_gray_left_of_yellow = False

                for gray_row, gray_col in gray_pixels:
                    if i == gray_row + 1:
                        is_below_gray = True
                    if j == gray_col + 1:
                        is_right_of_gray = True

                if is_below_gray and is_right_of_gray:
                        output_grid[i,j] = 4

                if is_right_of_gray:
                    if i > 0 and output_grid[i-1,j] == 4:
                          is_right_of_gray_above_yellow = True
                    elif i>1 and output_grid[i-2,j] == 4:
                        is_right_of_gray_above_yellow = True

                if is_below_gray:
                    if j > 0 and output_grid[i,j-1] == 4:
                        is_under_gray_left_of_yellow=True

                if is_right_of_gray_above_yellow:
                    output_grid[i,j] = 2
                elif is_under_gray_left_of_yellow:
                    output_grid[i,j] = 2
                elif i == 1 and j == 1:
                    output_grid[i,j] = 2

    return output_grid
```
