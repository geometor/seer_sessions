```python
"""
Transforms a 10x10 grid by expanding a single colored pixel in the last row into a repeating pattern across all rows. The pattern alternates the original color with grey (5) and black (0) based on the position of the original pixel. The last row contains 5.
"""

import numpy as np

def find_seed_pixel(grid):
    # Find the non-black pixel in the last row
    last_row = grid[-1]
    for x, color in enumerate(last_row):
        if color != 0:
            return x, color
    return None, None  # Should not happen, based on problem definition

def transform(input_grid):
    # Initialize output grid as all zeros
    output_grid = np.zeros_like(input_grid)

    # Find the seed pixel in the last row
    seed_x, seed_color = find_seed_pixel(input_grid)

    # Create and apply the repeating sequence for each row
    for y in range(output_grid.shape[0]):
        x = seed_x
        #apply seed color
        while x < output_grid.shape[1]:
          output_grid[y,x] = seed_color
          x+=2

        x = seed_x - 2
        while x >= 0:
          output_grid[y,x] = seed_color
          x -= 2
    
    # fill in gaps
    for y in range(output_grid.shape[0]):
      for x in range(output_grid.shape[1]):

        if output_grid[y,x] == seed_color:

          if x+1 < output_grid.shape[1]:
            if output_grid[y, x+1] == 0:
                output_grid[y, x+1] = 5

    # modify last row - add 5 to right of last seed color
    last_seed_x = -1
    for x in range(output_grid.shape[1]):
        if output_grid[-1, x] == seed_color:
            last_seed_x = x
    if last_seed_x != -1 and last_seed_x + 1 < output_grid.shape[1]:
      output_grid[-1, last_seed_x + 1] = 5

    return output_grid
```