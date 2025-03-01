"""
1.  **Maroon Pixel Duplication:** The maroon (9) pixel remains in its original row and column. A *new* maroon pixel is created in the row immediately below the original maroon pixel's column. If the original maroon pixel is on the bottom row, the duplicate also appears on the bottom row.

2.  **Azure Block Modification:**  The azure (8) pixel *directly* below the original maroon pixel becomes maroon (9). If there isn't an azure pixel directly below, then this step does *not* occur.

3.  **Magenta Pixel Repositioning:** The magenta (6) pixel is moved. The new location for the magenta is the left-most position of the lowest row of the azure block.

4.  **Yellow Pixel Invariance:** The yellow (4) pixel maintains its original position.

5. **Blank Spaces**: Empty spaces are filled with color black(0).
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of a single pixel of the specified color.
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0]  # Return the first occurrence
    return None

def find_block(grid, color):
    # Find coordinates of a block, assume its solid rectangle, find top left and bottom right
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
      min_row, min_col = np.min(coords, axis=0)
      max_row, max_col = np.max(coords, axis=0)
      return (min_row, min_col), (max_row, max_col)
    return None, None

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = input_grid.copy()
    
    # 1. Maroon Pixel Duplication
    maroon_pos = find_object(input_grid, 9)
    if maroon_pos is not None:
        output_grid[maroon_pos[0], maroon_pos[1]] = 9  # Keep original
        new_maroon_row = min(maroon_pos[0] + 1, output_grid.shape[0] - 1)
        output_grid[new_maroon_row, maroon_pos[1]] = 9  # Duplicate below

    # 2. Azure Block Modification
    _, (bottom_right_8, _) = find_block(input_grid, 8) #find azure block
    if maroon_pos is not None and bottom_right_8 is not None:
        target_row = maroon_pos[0] + 1
        if target_row < input_grid.shape[0] and input_grid[target_row, maroon_pos[1]] == 8:
          output_grid[target_row, maroon_pos[1]] = 9

    # 3. Magenta Pixel Repositioning
    magenta_pos = find_object(input_grid, 6)
    (top_left_8, _), (bottom_right_8, _) = find_block(input_grid, 8)

    if magenta_pos is not None and top_left_8 is not None:
      # Place magenta at leftmost of the azure block's bottom row.
      target_row = bottom_right_8[0]
      target_col = top_left_8[1]

      if 0 <= target_row < output_grid.shape[0] and 0<= target_col < output_grid.shape[1]:
          output_grid[magenta_pos[0], magenta_pos[1]] = 0  # Remove original
          output_grid[target_row, target_col] = 6


    # 4. Yellow Pixel Invariance (already handled by copying)
    
    # 5. Blank spaces remain 0 - they are 0 by default.
    
    return output_grid