# 10fcaaa3 • 018 • example_4 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1. Double the grid size: The output grid is twice the size of the input grid in both height and width (4x4 becomes 8x8).
2. Copy and Translate Red: The red pixel from the input grid is copied to the output grid at the multiplied coordinates of input (1,1) becoming output(1,1)
3. Horizontal Translation: Add 4 to the column. If result is within boundary, copy the red pixel.
4. Fill with Azure: Fill every other cell in output with azure (8). All odd columns in odd rows contain azure.
5. Retain Background: All white pixels(0) remains 0 at where they are without azure(8) or red(2).
"""

import numpy as np

def transform(input_grid):
    # Double the grid size
    input_height, input_width = input_grid.shape
    output_height, output_width = 2 * input_height, 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the red pixel in the input grid
    red_pixels = np.argwhere(input_grid == 2)

    # Copy and translate red pixel and check horizontal translation.
    for red_pixel in red_pixels:
      row, col = red_pixel
      output_grid[row*2-0, col*2-0] = 2

      new_col = (col*2-0) + 4
      if new_col < output_width:
          output_grid[row*2-0,new_col] = 2

    # Fill with azure, starting from top-left (0,0)
    for i in range(output_height):
        for j in range(output_width):
            if i % 2 == 0 and j % 2 == 0:
                output_grid[i, j] = 8
            
    return output_grid
```
