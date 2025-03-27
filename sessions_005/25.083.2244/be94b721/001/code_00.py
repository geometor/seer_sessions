"""
1. **Identify Target Object:** Scan the input grid to find the rightmost object.
    The color can be decided by getting the color that are not black/background.
    It should be positioned at the right of any other color.

2. **Extract:** Create an output by printing the selected pixels on a black background.
    Reshape by counting row and columns of the selected object.

3.  **Output:** The resulting cropped and potentially reshaped object is the output.
"""

import numpy as np

def find_rightmost_object(grid):
    """Finds the rightmost object in the grid and returns its color and bounding box."""
    rows, cols = grid.shape
    target_color = 0
    min_row, min_col = rows, cols
    max_row, max_col = 0, 0

    # Iterate through the grid to find the rightmost non-zero color
    for r in range(rows):
        for c in range(cols - 1, -1, -1):  # Iterate from right to left
            if grid[r, c] != 0:
                if target_color == 0:
                    target_color = grid[r, c]
                
                if grid[r,c] == target_color:
                  min_row = min(min_row, r)
                  min_col = min(min_col, c)
                  max_row = max(max_row, r)
                  max_col = max(max_col, c)
                break  # Move to the next row after finding a non-zero pixel
        
    if target_color ==0:
        return 0, None

    return target_color, (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """Transforms the input grid by extracting and reshaping the rightmost object."""
    # Find the rightmost object
    target_color, bbox = find_rightmost_object(input_grid)

    if target_color == 0 or bbox is None :
        return np.zeros((1,1), dtype=int)


    min_row, min_col, max_row, max_col = bbox

    # Extract the object and reshape based on I/0 examples
    object_rows = []
    
    input_rows, input_cols = input_grid.shape
    
    temp_object_rows = []

    for r in range(input_rows):
      row_pixels = []
      for c in range(input_cols):
        if input_grid[r,c] == target_color:
          row_pixels.append(input_grid[r,c])
        elif len(row_pixels) > 0:
            row_pixels.append(0)
      if len(row_pixels) > 0 :
        temp_object_rows.append(row_pixels)


    # padding 0 above the first row if the first row does not start at beginning.
    first_row = temp_object_rows[0]
    if first_row[0] == 0:
      padded_row = []
      for i in range(len(first_row)):
        if first_row[i] != 0:
            break
        padded_row.append(0)
      object_rows.append(padded_row)

    for row in temp_object_rows:
        object_rows.append(row)

    # padding 0 below the last row if the last row does not start at beginning.
    last_row = temp_object_rows[-1]
    if last_row[0] == 0 and len(object_rows) > len(object_rows[0]):
      padded_row = []
      for i in range(len(last_row)):
        if last_row[i] != 0:
            break
        padded_row.append(0)
      object_rows.append(padded_row)

    output_grid = np.array(object_rows)
    return output_grid