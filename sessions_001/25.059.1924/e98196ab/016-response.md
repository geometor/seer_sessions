# e98196ab • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Copy Red Pixels:** Copy locations of all red pixels (value 2) from the input grid to become the first row of the output grid.
2.  **Copy Blue Pixels:** Copy all blue pixels (value 1) from the input grid to the output grid, maintaining their relative positions.
3.  **Remove Gray Row:** Remove the entire horizontal row of gray pixels (value 5) from the input grid.
4.  **Transform Last Red:** Find the red pixel (2) located at the extreme bottom right of the *input* grid. Change this pixel to a blue pixel (1) in the last position in the *output* grid.
5. The last row on the input becomes the last row of the output with the exception of the transformation defined in step 4.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array.
    
    # Find coordinates of red and blue pixels.
    red_pixels = find_pixels_by_color(input_grid, 2)
    blue_pixels = find_pixels_by_color(input_grid, 1)

    # Determine the rows to keep (exclude gray row).
    gray_row_index = -1
    for i, row in enumerate(input_grid):
        if np.all(row == 5):
            gray_row_index = i
            break
            
    rows_to_keep = [i for i in range(input_grid.shape[0]) if i != gray_row_index]
    
    # create new output grid without the gray row
    output_grid = input_grid[rows_to_keep]

    # copy red pixel x coordinates to the first row of the output grid.
    if len(red_pixels) > 0:
      for coord in red_pixels:
          output_grid[0, coord[1]] = 2
    
    # Find the bottom-right red pixel in the *input* grid and change last one to blue (1) in *output*.
    red_pixels_in_last_row = []
    
    if gray_row_index == -1:
        last_row_input_index = input_grid.shape[0] - 1
    else:
        last_row_input_index = input_grid.shape[0] - 1

    
    for x,y in red_pixels:
        if x == last_row_input_index:
           red_pixels_in_last_row.append([x,y])    
    
    if len(red_pixels_in_last_row) > 0:
        last_red_pixel = max(red_pixels_in_last_row, key=lambda item: item[1])
        # change last red pixel to blue in last row
        output_grid[-1, last_red_pixel[1]] = 1

    return output_grid.tolist()
```
