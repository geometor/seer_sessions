"""
1.  **Identify Red Pixels:** Locate all red pixels (value 2) in the input grid.
2.  **Group by Row:** Group the red pixels by their row index. Sort the red pixels within each row by column.
3. **Conditional Color Change (Red to Yellow):**
   - Skip rows that have only red and white pixels.
   - For all other rows, iterate through the red pixels in each row:
      - If a red pixel is *not* the *first* occurring red pixel in the row and all pixels between the prior red pixel and this one are white, change the value of this (the second) red pixel to yellow (4).
4. **Vertical Yellow Propagation:** Iterate through each cell in the grid. If a cell is yellow (4), change the cell directly below it (if it exists) to yellow (4) as well.
5. If a row contains only red pixels and white pixels, no change is made.
"""

import numpy as np

def get_red_pixels(grid):
    # use where to find red pixels
    red_pixels = np.where(grid == 2)
    # combine and return list of (row, col)
    return list(zip(red_pixels[0], red_pixels[1]))

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    red_pixels = get_red_pixels(input_grid)
    
    # create dictionary, keys are row, values are column
    red_pixels_by_row = {}
    for r, c in red_pixels:
        if r not in red_pixels_by_row:
            red_pixels_by_row[r] = []
        red_pixels_by_row[r].append(c)

    # sort red pixels by column
    for row in red_pixels_by_row:
      red_pixels_by_row[row].sort()

    for row in red_pixels_by_row:
      # Skip if the row is entirely red or red/white
      all_red_or_white = True
      for c in range(cols):
        if output_grid[row, c] != 0 and output_grid[row,c] != 2:
          all_red_or_white = False
          break
      if all_red_or_white:
        continue

      col_indices = red_pixels_by_row[row]
      
      # check for more than one red in the row before iterating
      if len(col_indices) > 1:
        for i in range(1, len(col_indices)):  # Start from the *second* red pixel
            current_col = col_indices[i]
            previous_col = col_indices[i-1]
            
            # check if all are white between the two
            all_white = True
            for j in range(previous_col + 1, current_col):
              if output_grid[row, j] != 0:
                all_white = False
                break
            
            if all_white:
              output_grid[row, current_col] = 4

    # propagate yellow color down
    for r in range(rows - 1):
        for c in range(cols):
            if output_grid[r, c] == 4:
                output_grid[r + 1, c] = 4

    return output_grid