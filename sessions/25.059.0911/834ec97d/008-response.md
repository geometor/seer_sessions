# 834ec97d • 008 • refine_coder

---
```python
"""
1.  **Initialization:** Start with an output grid filled with zeros, the same size as the input grid.
2.  **Iterate through Red Pixels:** For *each* red pixel (value 2) found in the input grid:
    a. **Check Row:** Determine if the red pixel is in the last row.
    b. **Move Down (if not last row):** If the red pixel is *not* in the last row, place a red pixel one row below its current position in the *output* grid. Then, place a yellow pixel (value 4) at the red pixel's original position in the *output* grid.
    c. **Stay and Place Above (if last row):** If the red pixel *is* in the last row, place a red pixel at the same location in the *output* grid. Then, if there is space, place a yellow pixel one row *above* the red pixel in the output grid.
3.  **Preserve Yellow:** do not modify any cells with yellow in the input.
4. **All other cells:** all other cells should have a value of 0
"""

import numpy as np

def find_all_pixels_by_color(grid, color_value):
    # Find the coordinates of all pixels with the specified color value.
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Iterate through Red Pixels
    red_pixels = find_all_pixels_by_color(input_grid, 2)
    for red_pixel_pos in red_pixels:
        # Check Row
        if red_pixel_pos[0] < input_grid.shape[0] - 1:
            # Move Down (if not last row)
            new_red_pos = [red_pixel_pos[0] + 1, red_pixel_pos[1]]
            output_grid[new_red_pos[0], new_red_pos[1]] = 2
            output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 4
        else:
            # Stay and Place Above (if last row)
            output_grid[red_pixel_pos[0], red_pixel_pos[1]] = 2
            if red_pixel_pos[0] > 0:
                output_grid[red_pixel_pos[0] - 1, red_pixel_pos[1]] = 4

    # Preserve existing yellow pixels - this logic assumes yellow pixels don't move or get overwritten
    yellow_pixels = find_all_pixels_by_color(input_grid, 4)
    for yel_pixel_pos in yellow_pixels:
        output_grid[yel_pixel_pos[0], yel_pixel_pos[1]] = 4

    return output_grid
```

