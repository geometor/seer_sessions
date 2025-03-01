# e98196ab • 020 • refine_coder

---
```python
"""
1. **Red Pixel Consolidation:** For each column, if red pixels exist in that column in the input grid, the output grid will have a single red pixel in that column.
2. **Red Pixel Placement:** The red pixel in each column of the output grid is placed at the row index corresponding to the *number* of red pixels in that column in the input grid. If a column contains 3 red pixels in the input, the output will have a red pixel in the 3rd row (index 2) of that column.
3. **Rightmost Red to Blue (Last Row Only):** In the last row of the input grid, if there are any red pixels, the rightmost red pixel is changed to blue in the output grid. All other pixels remain unchanged, except for the red pixel movement described in 1 & 2.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # 1 & 2. Red Pixel Consolidation and Placement:
    for col in range(input_grid.shape[1]):
        red_pixels_in_col = [row for row in range(input_grid.shape[0]) if input_grid[row, col] == 2]
        if red_pixels_in_col:
            red_count = len(red_pixels_in_col)
            # Clear existing red pixels in that column of the output grid
            for row in red_pixels_in_col:
                output_grid[row, col] = 0
            # Place a single red pixel based on the count
            if red_count < output_grid.shape[0]:
                output_grid[red_count, col] = 2


    # 3. Rightmost Red to Blue (Last Row Only):
    last_row_index = input_grid.shape[0] - 1
    red_pixels_last_row = find_pixels_by_color(input_grid, 2)
    
    red_pixels_last_row_coords = []
    for x, y in red_pixels_last_row:
      if x == last_row_index:
        red_pixels_last_row_coords.append([x,y])
    
    if len(red_pixels_last_row_coords) > 0:
        last_red_pixel = max(red_pixels_last_row_coords, key=lambda item: item[1])
        output_grid[last_row_index, last_red_pixel[1]] = 1

    return output_grid.tolist()
```
