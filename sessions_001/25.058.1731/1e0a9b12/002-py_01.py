"""
The transformation rule is to consolidate all non-zero pixels to the bottom of the grid,
maintaining their relative horizontal order, and removing empty top rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving all non-zero pixels to the bottom,
    maintaining their relative horizontal order, and removing empty top rows.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Identify Non-Zero Pixels and their original positions
    non_zero_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                non_zero_pixels.append((input_grid[r, c], c)) # Store color and original column

    # 2. Sort non-zero pixels by their original column to maintain horizontal order
    non_zero_pixels.sort(key=lambda x: x[1])

    # 3. Create an empty output grid (initially same size as input)
    output_grid = np.zeros_like(input_grid)

    # 4. Place non-zero pixels at the bottom rows
    row_index = rows -1
    col_index_in_row = 0

    current_row = []
    for pixel, original_col in non_zero_pixels:
        current_row.append((pixel, original_col))

    filled_grid = np.zeros((len(current_row),cols))

    
    i = 0
    for pixel, original_col in non_zero_pixels:
      filled_grid[i%len(current_row)][original_col] = pixel
      i += 1


    # calculate the number of non-zero rows needed and remove blank rows at the top
    if len(current_row)>0:
        new_rows = max(1, (len(non_zero_pixels) + cols-1)//cols)
    else:
        new_rows = 0

    
    # 5. Create new output, resized based on number of non-zero rows
    
    if new_rows > 0:
      output_grid = np.zeros((new_rows, cols), dtype=int)
      for r in range(new_rows):
        for c in range(cols):
          output_grid[r,c]= filled_grid[r,c]

    return output_grid.tolist()