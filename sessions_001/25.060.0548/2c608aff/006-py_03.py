"""
1.  **Identify Key Pixels:** Locate all pixels with color green (3), yellow (4), and azure (8).

2.  **Green Region Influence:** Consider the rows containing the green (3) region.

3.  **Yellow Pixel Extension:** Yellow (4) pixels on rows containing green (3) extend to the left, replacing azure (8) pixels until a non-azure pixel is encountered.

4. **Yellow Pixels on Rows without Green**
    If a row with yellow pixels does *not* contain green:
    - If there's *more than one* yellow pixel, they all remain and extend.
    - extend to the left replacing any azure.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    return np.argwhere(grid == color)

def transform(input_grid):
    output_grid = np.copy(input_grid)
    green_pixels = find_pixels_by_color(input_grid, 3)
    yellow_pixels = find_pixels_by_color(input_grid, 4)

    # Determine rows with green pixels
    green_rows = np.unique(green_pixels[:, 0])

    # Handle yellow pixel extension
    for y_pixel in yellow_pixels:
        row, col = y_pixel
        if row in green_rows:
           # Extend yellow to the left on green rows
           for c in range(col -1, -1, -1):
               if output_grid[row,c] == 8:
                   output_grid[row,c] = 4
               else:
                   break # Stop if not azure
        else:
          #check if there are more than one yellow pixel on this row
          yellow_pixels_on_row = yellow_pixels[yellow_pixels[:,0] == row]
          if len(yellow_pixels_on_row) > 0:
            #extend yellow to left
            for c in range(col - 1, -1, -1):
              if output_grid[row,c] == 8:
                output_grid[row,c] = 4
              else:
                break

    return output_grid