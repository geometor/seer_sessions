```python
"""
1.  **Locate Orange Pixels:** Identify all pixels in the input grid that are colored orange (7).

2.  **Change to Magenta:** Change the color of all identified orange pixels to magenta (6).

3.  **Locate and change adjacent Azure:** Change the color of all identified adjacent azure pixels to magenta (6).

4.  **Other Border Changes:** Account for minor shifts/replacements between green(3)/azure(8) and, sometimes, white(0) pixels at the edges of other shapes. *This last step is not deterministic and I can't define the rule with only 2 examples.*
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Use numpy to find coordinates of all pixels matching the given color.
    return np.argwhere(grid == color)

def get_adjacent_pixels(grid, row, col):
    # returns the adjacent pixels to (row, col) but NOT including (row, col)
    height, width = grid.shape
    adjacent_pixels = []
    for i in range(max(0, row - 1), min(height, row + 2)):
        for j in range(max(0, col - 1), min(width, col + 2)):
            if (i, j) != (row, col):
                adjacent_pixels.append((i, j))
    return adjacent_pixels

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # find orange pixels to change to magenta
    orange_pixels = find_pixels_by_color(input_grid, 7)
    for row, col in orange_pixels:
        output_grid[row, col] = 6

    # Find and change adjacent azure(8) to magenta (6)
    for row, col in orange_pixels:
      adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
      for adj_row, adj_col in adjacent_pixels:
          if input_grid[adj_row, adj_col] == 8:
            output_grid[adj_row, adj_col] = 6

    # Find and change adjacent azure(8) to magenta (6) - repeat
    magenta_pixels = find_pixels_by_color(output_grid, 6)
    
    new_mag_pix = [] # make list because cannot change size of array while using
    for row, col in magenta_pixels:
      adjacent_pixels = get_adjacent_pixels(output_grid, row, col)
      for adj_row, adj_col in adjacent_pixels:
          if output_grid[adj_row, adj_col] == 8:
            new_mag_pix.append((adj_row, adj_col))

    for r, c in new_mag_pix:
      output_grid[r,c] = 6


    return output_grid
```