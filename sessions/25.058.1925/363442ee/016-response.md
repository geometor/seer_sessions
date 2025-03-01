# 363442ee • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify a vertical gray line (color 5) in the input grid.
2. Define the region to the left of this line as the "left region".
3. Copy the pattern of the left region and place it directly to the right of the gray line.
4. Repeat this pattern horizontally, wrapping to the next row when necessary, and filling the output grid. Stop when a blue pixel is encountered.
"""

import numpy as np

def find_vertical_line(grid, color):
    """Finds the x-coordinate of a vertical line of the specified color."""
    height, width = grid.shape
    for x in range(width):
        is_line = True
        for y in range(height):
            if grid[y, x] != color:
                is_line = False
                break
        if is_line:
            return x
    return -1  # Not found

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, width), dtype=int)

    # 1. Identify the Separator
    separator_x = find_vertical_line(input_grid, 5)

    # 2. Define Left Region
    left_region = input_grid[:, :separator_x]
    left_height, left_width = left_region.shape

    # 3 & 4. Copy, Shift, Repeat and Wrap
    dest_x = separator_x + 1
    for y in range(height):
        for x_offset in range(width - dest_x):
            # Check for any blue pixels
            blue_present = False
            for scan_y in range(height) :
                if input_grid[scan_y,x_offset+dest_x] == 1 :
                    blue_present = True
                    break

            output_x = dest_x + x_offset
            if output_x < width and not blue_present:  # Stay within bounds
              output_grid[y, output_x] = left_region[y % left_height, x_offset % left_width]
            
    # transfer over original values from input grid, except not the grey separator line
    for y in range(height):
        for x in range(width):
          if x != separator_x:
            output_grid[y,x] = input_grid[y,x]

    # now transfer over the shifted values.
    dest_x = separator_x + 1
    for y in range(height):
        for x_offset in range(width - dest_x):
          
            output_x = dest_x + x_offset
            if output_x < width:  # Stay within bounds
              output_grid[y, output_x] = left_region[y % left_height, x_offset % left_width]

    return output_grid
```
