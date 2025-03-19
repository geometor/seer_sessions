# 29c11459 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Objects:** Locate the blue pixel (1) and the red pixel (2) within the input grid. Note their positions.
2.  **Determine Midpoint:** Calculate the horizontal midpoint between the blue and red pixels. If the distance between them is odd there will be one pixel at the midpoint position. If the distance is even, the midpoint will be between two pixels.
3. **Fill Left Segment:** Change all the pixels horizontally to the left side of the midpoint on the same row to blue (1).
4. **Place Middle Pixel:** Place a single grey pixel (5) on the same row at the midpoint.
5.  **Fill Right Segment:** Change all pixels horizontally to the right side of the midpoint on the same row to red (2).
6. **Preserve Other Pixels:** Ensure all other pixels in the grid retain their original colors.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a pixel of the given color."""
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)  # Return row and column index.
    return None  # If not found.

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find the blue and red pixels
    blue_pos = find_pixel(input_grid, 1)
    red_pos = find_pixel(input_grid, 2)

    # proceed only if both pixels are found
    if blue_pos is not None and red_pos is not None:
      
        # get the row that will change
        row_index = blue_pos[0]

        # calculate midpoint
        midpoint = (blue_pos[1] + red_pos[1]) // 2

        # fill left segment with blue
        for i in range(blue_pos[1] + 1, midpoint):
            output_grid[row_index, i] = 1

        # place middle grey pixel
        output_grid[row_index, midpoint] = 5
        
        # fill right segment with red
        for i in range(midpoint + 1, red_pos[1]):
            output_grid[row_index, i] = 2
    
    # return the transformed grid
    return output_grid
```
