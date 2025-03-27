"""
1.  **Identify the Top-Left Object:** Locate the contiguous block of pixels in the top-left corner of the input grid that consists of blue (1) and/or white (0) pixels.
2.  **Determine Dimensions:** Calculate the width (number of columns) and height (number of rows) of this top-left object.
3. **Extract Sub-grid:** Create a new grid with the dimensions determined in step 2.
4.  **Copy Pixels:** Copy the pixel values from the input grid, starting at the top-left corner (0,0) and extending to the calculated width and height, to the corresponding positions in the new output grid.
"""

import numpy as np

def get_object_dimensions(grid):
    """Helper function to determine the dimensions of top-left object"""
    rows, cols = grid.shape
    
    # Find the first non-blue/white cell row
    max_row = 0
    for r in range(rows):
        is_object_row = False
        for c in range(cols):
            if grid[r,c] == 0 or grid[r,c] == 1:
                is_object_row = True
                break
        if is_object_row:
            max_row += 1
        else:
             break

    #find the first non-blue/white cell column

    max_col = 0
    for c in range(cols):
      is_object_col = False
      for r in range(rows):
        if grid[r,c] == 0 or grid[r,c] == 1:
          is_object_col = True
          break
      if is_object_col:
        max_col+=1
      else:
        break

    return max_row, max_col
def transform(input_grid):
    """Transforms the input grid by extracting the top-left object."""
    input_grid = np.array(input_grid)

    # Determine dimensions of the top-left object
    height, width = get_object_dimensions(input_grid)

    # Create output grid and copy pixels
    output_grid = np.zeros((height, width), dtype=int)

    for r in range(height):
      for c in range(width):
        output_grid[r,c] = input_grid[r,c]
    return output_grid.tolist()