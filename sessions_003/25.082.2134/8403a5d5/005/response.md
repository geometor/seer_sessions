```python
"""
Transforms a 10x10 grid by expanding a single colored pixel in the last row into a repeating pattern across all rows. The pattern alternates the original color with grey (5) and black (0) based on the position of the original pixel.
"""

import numpy as np

def find_seed_pixel(grid):
    """Finds the non-black pixel in the last row."""
    last_row = grid[-1]
    for x, color in enumerate(last_row):
        if color != 0:
            return x, color
    return None, None  # Should not happen

def transform(input_grid):
    """Transforms the input grid based on the seed pixel."""
    output_grid = np.zeros_like(input_grid)
    seed_x, seed_color = find_seed_pixel(input_grid)

    if seed_x is None:
        return output_grid  # Should not happen, based on problem definition

    for y in range(output_grid.shape[0]):
        # Fill to the right
        x = seed_x
        while x < output_grid.shape[1]:
            output_grid[y, x] = seed_color
            x += 1
            if x < output_grid.shape[1]:
                output_grid[y, x] = 5
            x += 1

        # Fill to the left
        x = seed_x - 1
        while x >= 0:
            if (seed_x - x) % 2 == 1:
                output_grid[y,x] = 5
            else:
                output_grid[y,x] = 0
            
            x -= 1
        
        # correct for seed color
        x = seed_x -2
        while x >= 0:
            output_grid[y,x] = seed_color
            x -= 2

    # Last row modification
    for x in range(output_grid.shape[1] - 1):  # Iterate up to the second-to-last column
        if output_grid[-1,x] == seed_color:
            if (x - seed_x) % 2 == 0:
                if output_grid[-1, x+1] == 0:
                     output_grid[-1, x + 1] = 5

    return output_grid
```