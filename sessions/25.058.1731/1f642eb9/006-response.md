# 1f642eb9 • 006 • refine_coder

---
```python
"""
1.  **Maroon Pixel Duplication:** The maroon (9) pixel remains in its original row. A new maroon pixel is created in the row immediately below the original maroon pixel's column. If the original maroon pixel is on the bottom row, the new maroon pixel will appear on the bottom row.

2.  **Azure Block Modification:** An azure (8) pixel within the azure block that is directly below the original maroon pixel, becomes maroon (9). This assumes there is always at least one azure pixel below the maroon one.

3.  **Magenta Pixel Repositioning:** The magenta (6) pixel is moved to a new position. The preferred new position is directly below the azure block, and left aligned with its left most boundary. If the azure block occupies the lowest rows, the magenta pixel moves to the lowest available row, adjacent to the azure block on either the left or right side, whichever provides available space.

4.  **Yellow Pixel Invariance:** The yellow (4) pixel maintains its original position in the grid.

5.  **Blank Spaces**: Empty spaces are filled with color black(0).
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
    (top_left_8, _), _ = find_block(input_grid, 8)
    if top_left_8 is not None and maroon_pos is not None:
      if top_left_8[0] <= maroon_pos[0]: # check if block begins before maroon
        target_row = maroon_pos[0] + 1
      else:
        target_row = top_left_8[0]
      
      if target_row < input_grid.shape[0]:  # Check for out-of-bounds access
          if input_grid[target_row, maroon_pos[1]] == 8:  # find azure pixel in the same column.
            output_grid[target_row, maroon_pos[1]] = 9 # make it maroon

    # 3. Magenta Pixel Repositioning
    magenta_pos = find_object(input_grid, 6)
    (top_left_8, _), (bottom_right_8, _) = find_block(input_grid, 8)

    if magenta_pos is not None and top_left_8 is not None:
      # Try to place it below the block
      target_row = bottom_right_8[0] + 1
      target_col = top_left_8[1]
      
      if target_row >= output_grid.shape[0]:
        # Not enough space below, try sides
        target_row = bottom_right_8[0]
        
        #try left first
        target_col = top_left_8[1] - 1
        if target_col < 0: #try right
            target_col = bottom_right_8[1] + 1

      if 0 <= target_row < output_grid.shape[0] and 0 <= target_col < output_grid.shape[1]: #check if valid position
        output_grid[target_row, target_col] = 6
        if (target_row != magenta_pos[0]) or (target_col != magenta_pos[1]):  # remove only if moved
          output_grid[magenta_pos[0], magenta_pos[1]] = 0 # Remove original
      else:
        output_grid[magenta_pos[0], magenta_pos[1]] = 0 # remove and don't put down


    # 4. Yellow Pixel Invariance (already handled by copying)
    
    # 5. Blank spaces remain 0 - they are 0 by default.
    
    return output_grid
```

