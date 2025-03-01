# f2829549 • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the vertical blue stripe:** Locate the single-pixel-wide, full-height vertical stripe of blue (value 1) pixels in the input grid.

2.  **Determine Output Grid Dimensions:** the output width is 3, the height is the same as the input

3.  **Construct output**: Create an output grid with height equal to the height of the input, and width 3.

4.  **Populate the output grid:**
    - The middle column is all white (0) pixels.
    - Output pixels to the left or the right are green, at row indeces offset by one.
    - if a green pixel would be placed outside the boundaries, do not place a green pixel
    - all other pixels are white (0).
"""

import numpy as np

def find_vertical_stripe(grid, color):
    # Find the column index of the vertical stripe of the specified color
    height = grid.shape[0]
    for col in range(grid.shape[1]):
        if all(grid[row, col] == color for row in range(height)):
            return col
    return -1  # Return -1 if no such stripe is found

def transform(input_grid):
    # Find the column index of the blue vertical stripe (color 1)
    blue_stripe_col = find_vertical_stripe(input_grid, 1)

    # Initialize the output grid with all white pixels (color 0)
    output_height = input_grid.shape[0]
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # if no blue stripe is found, just return a blank grid of the appropriate size
    if (blue_stripe_col == -1):
        return output_grid

    # Populate the output grid based on the blue stripe's position
    
    # middle column all white
    
    # set pixels to green (3) in "mirrored-L" shapes
    if output_height > 1:
        output_grid[output_height - 2, 0] = 3
        output_grid[output_height - 1, 2] = 3
        
        if output_height > 2:
             output_grid[1,0] = 3

    return output_grid
```
