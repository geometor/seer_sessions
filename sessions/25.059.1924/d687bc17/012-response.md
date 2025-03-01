# d687bc17 • 012 • refine_coder

---
```python
"""
1.  **Preserve the Border:** The outermost border of the grid, defined as all pixels on the top, bottom, left, and right edges, remains unchanged.
2.  **Clear Non-Border Pixels:** All pixels *not* on the border are set to color 0 (white).
3.  **Add a colored line:** Add a vertical line of pixels of the same color to the right border. The length is 1 unless there is a gap in the right edge, then the length is equal to the distance to fill the gap. The color of this vertical line is the same as the color of the last pixel before the gap.
4.  **Add a colored pixel:** find the last non-zero, non-border pixel in the input, looking from bottom to top, right to left. Add one pixel of a *different* color in a constant relative position. This position is the row of the last pixel -2, and the column 1.
"""

import numpy as np

def get_border_pixels(grid):
    """Returns a dictionary of border pixels."""
    rows, cols = grid.shape
    border = {
      "top": [(0,j) for j in range(cols)],
      "bottom": [(rows-1, j) for j in range(cols)],
      "left": [(i,0) for i in range(rows)],
      "right": [(i, cols-1) for i in range(rows)],
    }

    return border

def find_last_non_zero_non_border(grid):
    """Finds the last non-zero, non-border pixel in the input grid."""
    rows, cols = grid.shape
    border_pixels = get_border_pixels(grid)
    all_border_pixels = []

    for positions in border_pixels.values():
        all_border_pixels.extend(positions)

    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if (r, c) not in all_border_pixels and grid[r, c] != 0:
                return (r, c)
    return None

def get_right_border_color(grid):
    """Gets the color of the right border, handling gaps."""
    rows, cols = grid.shape
    border_pixels = get_border_pixels(grid)
    right_border = border_pixels['right']

    for i in range(rows - 2, -1, -1):  # Iterate upwards from second-to-last row
      if (i, cols-1) in right_border:
        if grid[i, cols-1] != 0:
            return grid[i,cols-1], i #color and start row
    return 0, 0 #return default if no non-zero

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get border pixels
    border_pixels = get_border_pixels(input_grid)
    all_border_pixels = []
    for positions in border_pixels.values():
        all_border_pixels.extend(positions)

    # Clear non-border pixels
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in all_border_pixels:
                output_grid[i, j] = 0

    # Add colored line to right border
    right_border_color, start_row = get_right_border_color(input_grid)

    #fill gap on right border if exists
    if start_row < rows -1 :
      for r in range(start_row, rows-1):
        output_grid[r, cols-1] = right_border_color


    # Add a colored pixel
    last_pixel_pos = find_last_non_zero_non_border(input_grid)
    if last_pixel_pos:
        new_row = last_pixel_pos[0] - 2
        new_col = 1

        #find different color than the last_pixel
        last_pixel_color = input_grid[last_pixel_pos]
        output_colors = np.unique(output_grid)

        new_color = last_pixel_color
        for c in range(10): #check for available colors
            if c not in output_colors:
                new_color = c
                break
        if 0 <= new_row < rows:  # Ensure new position is within bounds
                output_grid[new_row, new_col] = new_color


    return output_grid
```
