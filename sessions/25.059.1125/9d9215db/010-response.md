# 9d9215db • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Green Pixel Movement:** For each green pixel (3) in the input, move its y position. if the original y position is less than the center Y, increase the y by one. If the original y position if greater than the center Y, reduce it by one.

2.  **Blue and Yellow Pixel Mirroring:** Identify the central horizontal axis of the grid (y=9). For the blue (1) and yellow(4) pixels , mirror their position across this central axis. The new y-coordinate will be `new_y = (grid_height - 1) - old_y`

3. **Blue Pixel Expansion**: For each original and newly mirrored blue pixel, create copies of it by repeating the blue color to the left until the x coordinate 3 and right until the x coordinate 15.

4.  All other cells remain unchanged (value 0).
"""

import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]
    grid_width = output_grid.shape[1]
    center_y = grid_height // 2

    # Green Pixel Movement
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 3:
                if y < center_y:
                  output_grid[y,x] = 0
                  output_grid[y + 1, x] = 3
                elif y > center_y:
                  output_grid[y,x] = 0
                  output_grid[y - 1, x] = 3

    # Blue and Yellow Pixel Mirroring and Expansion
    for y in range(grid_height):
        for x in range(grid_width):
            if input_grid[y, x] == 1 or input_grid[y,x] == 4:
                new_y = (grid_height - 1) - y
                if input_grid[y,x] == 1:
                  output_grid[y,x] = 0
                  output_grid[new_y, x] = 1

                  # expand
                  for i in range(3,16):
                      output_grid[new_y,i] = 1

                elif input_grid[y,x] == 4:
                    output_grid[y,x] = 0
                    output_grid[new_y, x] = 4


    return output_grid
```
