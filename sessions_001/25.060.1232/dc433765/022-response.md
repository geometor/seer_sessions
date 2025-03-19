# dc433765 • 022 • example_4 • investigate_coder

---
```python
"""
1.  **Identify:** Locate the green pixel (value 3) and the yellow pixel (value 4) within the input grid. All the rest of the pixels are white(value 0).
2.  **Move:** Move the green pixel one row down, from its initial position (r,c) to position (r+1, c).
3. **Preserve other pixel positions**: Keep the position for all other pixels from the input grid to the output grid.
4.  **Output:** Create the output grid with the updated position of the green pixel, and keep all the positions unchanged for all other pixels.
"""

import numpy as np

def find_pixel(grid, color_value):
    # find the coordinates of a pixel with a specified color value
    coords = np.where(grid == color_value)
    if len(coords[0]) > 0:  # Check if the pixel exists
       return (coords[0][0], coords[1][0])
    else: return None

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)

    # find the green pixel
    green_pixel_coords = find_pixel(input_grid, 3)

    # Move the green pixel one row down if found
    if green_pixel_coords:
        r, c = green_pixel_coords
        output_grid[r, c] = 0  # remove from the original position
        output_grid[r + 1, c] = 3  # place in the new position
        
    return output_grid
```
