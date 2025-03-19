# 31aa019c • 008 • example_1 • investigate_coder

---
```python
"""
Identify the largest contiguous block of red (2) pixels in the input grid.
Replicate this red block to the sixth and seventh and eighth rows,
maintaining the shape of the input block.
Keep yellow pixel from the input block.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    # Initialize the output grid with all white pixels (0).
    output_grid = np.zeros_like(input_grid)

    # Find all red pixels.
    red_pixels = find_object(input_grid, 2)

    # Find yellow pixels.
    yellow_pixels = find_object(input_grid, 4)
    
    # Fill sixth, seventh and eight rows
    if len(red_pixels) > 0:
      for i in range(red_pixels.shape[0]):
        row = 6 + i if i < 3 else 7
        col = red_pixels[i][1]
        output_grid[row-1, col] = 2

    if len(yellow_pixels) > 0:
        row = yellow_pixels[0][0]
        col = yellow_pixels[0][1]
        #translate to the new red block
        if row >= 5 and row <=7:
            output_grid[row, col] = 4
        

    return output_grid
```
