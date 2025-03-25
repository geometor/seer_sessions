"""
1.  **Identify the Center:** Find the central element(s) of the input grid. The "center" can be a single element (in grids with odd dimensions) or a group of elements (in grids with even dimensions).

2.  **Central Replacement:** Replace the value(s) of the central element(s) in the input grid with 0 in the output grid.

3. **Diagonal Replacement:** Check the digits that are located *one step* diagonally from each of the central pixel(s) found in step 1.

4.  **Surrounding Replacement:** The value of these diagonally positioned digits is replaced with 0 in the output grid, if and only if the digit's value is different than the value of the center pixel.

5. **Copy Other Values:** All other elements that are *not* the center or one-step diagonal, keep their original values from the input grid to the output grid.
"""

import numpy as np

def get_center_indices(grid):
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2

    if rows % 2 == 0 and cols % 2 == 0:
        return [(center_row - 1, center_col - 1), (center_row - 1, center_col), (center_row, center_col - 1), (center_row, center_col)]
    elif rows % 2 == 0:
        return [(center_row - 1, center_col), (center_row, center_col)]
    elif cols % 2 == 0:
        return [(center_row, center_col - 1), (center_row, center_col)]
    else:
        return [(center_row, center_col)]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_indices = get_center_indices(input_grid)

    # Central Replacement
    for r, c in center_indices:
      output_grid[r, c] = 0
    
    # Diagonal Replacement and Surrounding check
    center_values = [input_grid[r,c] for (r,c) in center_indices]
    
    for row, col in center_indices:
      center_val = input_grid[row,col]

      for dr in [-1, 1]:
          for dc in [-1, 1]:
              new_row, new_col = row + dr, col + dc
              if 0 <= new_row < rows and 0 <= new_col < cols:
                  if input_grid[new_row, new_col] != center_val:
                      output_grid[new_row, new_col] = 0

    return output_grid