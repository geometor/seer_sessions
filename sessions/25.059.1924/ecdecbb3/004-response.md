# ecdecbb3 • 004 • example_1 • investigate_coder

---
```python
"""
1. **Identify Red Pixels:** Locate all red (2) pixels in the input grid.

2. **Vertical Extension:** For each red pixel, extend it vertically upwards and downwards, replacing white pixels with copies of the red one. Do this until the top and bottom edges of the grid are reached by the red shape.

3. **Azure Pixel Modification:**
    * Examine all azure (8) pixels.
    * If an azure pixel is directly adjacent to a vertically extended red pixel created in step 2 (above, below, to the left, or the right, but not diagonal), change its color to red (2).
    * Create white pixels (0) between areas of red and azure, if necessary.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds the coordinates of all red pixels in the grid."""
    red_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_index, col_index))
    return red_pixels

def get_azure_pixels(grid):
    """Finds the coordinates of all azure pixels in the grid."""
    azure_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 8:
                azure_pixels.append((row_index, col_index))
    return azure_pixels

def is_adjacent(coord1, coord2):
    """Checks if two coordinates are adjacent (not diagonally)."""
    row1, col1 = coord1
    row2, col2 = coord2
    return (abs(row1 - row2) <= 1 and col1 == col2) or \
           (abs(col1 - col2) <= 1 and row1 == row2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    grid_height = len(input_grid)

    # 1. Identify Red Pixels
    red_pixels = get_red_pixels(input_grid)

    # 2. Vertical Extension
    for red_pixel in red_pixels:
        row, col = red_pixel
        # Extend upwards
        for r in range(row - 1, -1, -1):
            output_grid[r, col] = 2
        # Extend downwards
        for r in range(row + 1, grid_height):
            output_grid[r, col] = 2

    # 3. Azure Pixel Modification
    azure_pixels = get_azure_pixels(input_grid)
    for azure_pixel in azure_pixels:
      row, col = azure_pixel
      
      is_adj_to_red = False
      for r in range(len(output_grid)):
        if is_adjacent((r, col), (r,col)) and output_grid[r,col] == 2:
          is_adj_to_red = True
          break
      if is_adj_to_red:
        output_grid[row,col] = 2
      
    # now, set to zero any azure that does *not* touch a red
    azure_pixels = get_azure_pixels(output_grid)
    for azure_pixel in azure_pixels:
      row, col = azure_pixel
      
      is_adj_to_red = False
      for r in range(len(output_grid)):
        if is_adjacent((r, col), (r,col)) and output_grid[r,col] == 2:
          is_adj_to_red = True
          break
      if not is_adj_to_red:
        output_grid[row,col] = 0
        

    return output_grid
```
