# 3bd67248 • 012 • refine_coder

---
```python
"""
1.  **Gray Anchors:** Identify all gray pixels (value 5) in the input grid. These pixels remain unchanged.
2.  **White Pixel Transformation:** Iterate through all white pixels (value 0) in the input grid.
3.  **Conditional Color Changes:**
    *   If a white pixel is *directly above* and *directly to the right* of a gray pixel, change it to red (2).
    *    If a white pixel is *directly below* a gray pixel *and* at the top left corner, change it to red (2).
    *   If a white pixel is *directly below* a gray pixel *and* *directly to the left* of a yellow pixel, change to red (2).
    *   If a white pixel is *directly below* and *directly to the right* of a gray pixel, change it to yellow (4).
    *   If a white pixel is *directly to the right* of a gray pixel *and* there is a yellow pixel either one or two rows *directly above*, change it to red.
    * If a white pixel is at the top left, and is to the right of a gray pixel, change it to red (2).

4. **Grid Update**: Apply all color changes to create the output grid.
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
    # initialize output_grid
    output_grid = np.copy(input_grid)
    gray_pixels = get_gray_pixels(input_grid)

    # change output pixels
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 0:  # White pixel
                is_directly_above_right_of_gray = False
                is_directly_below_left_of_yellow = False
                is_directly_below_right_of_gray = False
                is_right_of_gray_above_yellow = False
                is_top_left_right_of_gray = False
                is_directly_below_gray_top_left_corner = False

                for gray_row, gray_col in gray_pixels:
                    # Directly above and directly to the right of a gray pixel
                    if i == gray_row - 1 and j == gray_col + 1:
                        is_directly_above_right_of_gray = True

                    # Directly below a gray pixel and directly to the left of a yellow
                    if i == gray_row + 1 and j > 0 and output_grid[i, j-1] == 4:
                        is_directly_below_left_of_yellow = True

                    # Directly below and directly to the right of gray
                    if i == gray_row + 1 and j == gray_col + 1:
                        is_directly_below_right_of_gray = True
                    
                    # Directly below a gray, top left
                    if i == gray_row + 1 and i == 1 and j == 0:
                        is_directly_below_gray_top_left_corner = True

                    # Directly to right of gray and yellow above
                    if j == gray_col + 1 and ( (i > 0 and output_grid[i-1,j] == 4) or (i > 1 and output_grid[i-2, j] == 4) ):
                        is_right_of_gray_above_yellow = True
                    
                    # top left, and is to the right of gray
                    if i == 0 and j == 1 and gray_col == 0:
                        is_top_left_right_of_gray = True

                if is_directly_above_right_of_gray:
                    output_grid[i, j] = 2
                elif is_directly_below_left_of_yellow:
                    output_grid[i,j] = 2
                elif is_directly_below_right_of_gray:
                    output_grid[i, j] = 4
                elif is_right_of_gray_above_yellow:
                    output_grid[i,j] = 2
                elif is_top_left_right_of_gray:
                    output_grid[i,j] = 2
                elif is_directly_below_gray_top_left_corner:
                    output_grid[i,j] = 2

    return output_grid
```
