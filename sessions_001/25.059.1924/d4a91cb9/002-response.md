# d4a91cb9 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule identifies two non-zero pixels (StartPixel and EndPixel) in the input grid and connects them with an L-shaped path of color 4 (yellow) in the output grid. The original colors of the StartPixel and EndPixel are preserved.
"""

import numpy as np

def find_pixels(grid):
    # Find coordinates of non-zero pixels
    pixels = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                pixels.append((r, c, value))
    return pixels

def construct_l_path(grid, start_pixel, end_pixel):
    # Create a copy of the input grid to modify
    output_grid = np.copy(grid)

    start_row, start_col, start_value = start_pixel
    end_row, end_col, end_value = end_pixel

    # Preserve start and end pixel colors
    output_grid[start_row, start_col] = start_value
    output_grid[end_row, end_col] = end_value

    # Construct L-shaped path (vertical then horizontal)
    current_row = start_row
    current_col = start_col

    while current_row != end_row:
        if current_row < end_row:
            current_row += 1
        else:
            current_row -= 1
        output_grid[current_row, current_col] = 4

    while current_col != end_col:
        if current_col < end_col:
            current_col += 1
        else:
            current_col -= 1
        output_grid[current_row, current_col] = 4


    return output_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    
    # Find the start and end pixels.
    pixels = find_pixels(input_grid)
    
    if len(pixels) !=2:
      return output_grid

    start_pixel = pixels[0]
    end_pixel = pixels[1]

    # change output pixels 
    output_grid = construct_l_path(input_grid, start_pixel, end_pixel)

    return output_grid.tolist()
```
