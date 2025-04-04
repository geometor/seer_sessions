"""
1.  **Identify Key Pixels:** Locate all pixels with the color green (3) and yellow (4).

2.  **Green Region Influence:** Consider the rows containing the green (3) region.

3.  **Yellow Pixel Extension:** Identify the yellow (4) on row 7. It extends to the left, changing all azure (8) pixels to yellow (4) on those rows, and stops when there are no more azure pixels before hitting the green region.

4.  **Isolated Yellow Pixel:** The yellow (4) that is alone and is on the same rows as the green pixel is not extended. The single yellow pixel on a row that does not contain any green is deleted/turned azure.
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
           #check every row to do horizontal expansion toward left
           for c in range(col -1, -1, -1):
               if output_grid[row,c] == 8:
                   output_grid[row,c] = 4
               else:
                   break #stop if not azure
        elif row not in green_rows and len(yellow_pixels)>1: #if it is not within green row, delete
            output_grid[row,col] = 8
    
    #handle extending the yellow pixel on row 7
    yellow_pixels_row_7 = yellow_pixels[yellow_pixels[:,0]==7]
    if len(yellow_pixels_row_7)>0:
      row = 7
      col = yellow_pixels_row_7[0,1]
      for c in range(col-1, -1, -1):
        if output_grid[row,c] == 8:
          output_grid[row,c] = 4
        else:
          break

    return output_grid