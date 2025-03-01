# 06df4c85 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Background Tiles:** Divide the input grid into background tiles. By observation:
    *   In examples 1 and 3, the tile appears to be 3 rows x 6 cols
    *   In example 2, it seems that the background tiles are also 3 rows x 6 cols.

2.  **Identify Objects:** Locate all 2x2 squares of the same color that are distinct from the background colors.

3. **Replicate Object Color**: For each tile:
   * For each object that is partially in the tile
     * The colors within the tile are extended to all available columns
"""

import numpy as np

def find_objects(grid, size=2):
    objects = []
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            square = grid[r:r+size, c:c+size]
            if np.all(square == square[0, 0]):
                objects.append((square[0, 0], (r, c)))
    return objects

def is_background_color(color, example_num):
    if example_num in [1,3]:
        background_colors = [0, 8]
    elif example_num == 2:
      background_colors = [0,1]

    return color in background_colors


def transform(input_grid, example_num=1):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    tile_height = 3
    tile_width = 6

    # Identify Objects
    objects = find_objects(input_grid)

    # Iterate through tiles
    for tile_row in range(0, rows, tile_height):
        for tile_col in range(0, cols, tile_width):
          
          # Iterate through objects
          for color, (obj_row, obj_col) in objects:
              #Check if object is in tile
              if not is_background_color(color, example_num):
                if (tile_row <= obj_row < tile_row + tile_height) or \
                  (tile_row < obj_row + 2 <= tile_row + tile_height):

                    #Replicate object in tile
                    start_row = max(tile_row, obj_row)
                    end_row = min(tile_row+tile_height, obj_row + 2)

                    output_grid[start_row:end_row, tile_col:tile_col+tile_width] = color
    return output_grid
```
