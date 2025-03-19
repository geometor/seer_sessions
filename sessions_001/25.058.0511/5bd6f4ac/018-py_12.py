"""
1.  **Identify Source Row:** Determine the source row index within the input grid. The second example uses row index 1 (the second row), and the third uses row index 2 (the third row). Example 4 uses row index 1.
2.  **Output Grid:** Create output grid, size is always 3x3.
3. **Fill Output**: Fill in non-white values from the identified source row.
4. **All other values**: are 0 (white)
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid filled with zeros (white).
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine the source row index.  Prioritize row 1, then row 2.
    if input_grid.shape[0] > 1:
        source_row = input_grid[1, :]
    elif input_grid.shape[0] > 2:
        source_row = input_grid[2, :]
    else:
       return output_grid # return blank output if no valid source row

    # Filter out white pixels (0) from the source row.
    non_white_pixels = source_row[source_row != 0]

    # If the source row has non-white uniform color use it to populate the whole grid
    if np.all(non_white_pixels == non_white_pixels[0]) and len(non_white_pixels) > 0:
        output_grid[:] = non_white_pixels[0]
    else:
      # Populate output with non-white
      row, col = 0, 0
      for pixel in non_white_pixels:
          output_grid[row, col] = pixel
          col += 1
          if col > 2:  # Move to the next row if we exceed column 2.
              col = 0
              row += 1
          if row > 2:  # Stop if we exceed row 2
              break

    return output_grid