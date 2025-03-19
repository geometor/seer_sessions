# 11852cab • 012 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all red pixels (value 2) in the input grid.
2. **Determine Horizontal Extensibility** For any set of horizontally adjacent red pixels:
    *   Extend the red pixels to the left by adding one red pixel, if the extension is within the boundaries of the array, and the pixel to be changed is black (value 0)
    *  Extend the red pixels to the right by adding one red pixel, if the extension is within the boundaries of the array, and the pixel to be changed is black (value 0)
3. **Preserve other colored pixels:** Keep all non-red, non-black pixels in their original positions and colors.
4. If no red pixels are present, return the grid unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # If no red pixels, return original grid
    if len(red_pixels) == 0:
      return output_grid

    # Group horizontally adjacent red pixels
    red_groups = []
    if len(red_pixels) > 0:
      current_group = [red_pixels[0]]
      for i in range(1, len(red_pixels)):
        if red_pixels[i][0] == red_pixels[i-1][0] and red_pixels[i][1] == red_pixels[i-1][1] + 1:
            current_group.append(red_pixels[i])
        else:
          red_groups.append(current_group)
          current_group = [red_pixels[i]]
      red_groups.append(current_group)

    # Extend red groups horizontally
    for group in red_groups:
      # Extend left
      leftmost_pixel = group[0]
      if leftmost_pixel[1] > 0 and output_grid[leftmost_pixel[0], leftmost_pixel[1]-1] == 0:
          output_grid[leftmost_pixel[0], leftmost_pixel[1] - 1] = 2

      # Extend right
      rightmost_pixel = group[-1]
      if rightmost_pixel[1] < cols - 1 and output_grid[rightmost_pixel[0], rightmost_pixel[1]+1] == 0:
        output_grid[rightmost_pixel[0], rightmost_pixel[1] + 1] = 2

    return output_grid
```
