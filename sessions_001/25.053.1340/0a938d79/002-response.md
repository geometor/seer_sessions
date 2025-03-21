# 0a938d79 • 002 • example_1 - CODE

---
```python
"""
Transforms an input grid by identifying non-white pixels (seeds) and expanding them into an alternating checkerboard pattern of red and azure, maintaining the original grid's dimensions, and filling the rest with white.
"""

import numpy as np

def find_seed_pixels(grid):
    """Finds non-white pixels in the grid."""
    seeds = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel != 0:
                seeds.append((r, c, pixel))
    return seeds

def transform(input_grid):
    """Transforms the input grid according to the checkerboard rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_cols = cols

    # Find seed pixels and their colors.
    seed_pixels = find_seed_pixels(input_grid)
    if not seed_pixels:  # Handle cases with no seed pixels.
        return np.zeros((rows, output_cols), dtype=int).tolist()

    seed_colors = [pixel[2] for pixel in seed_pixels]
    if len(seed_colors) < 2 :
      first_color = seed_colors[0]
      if (first_color == 2):
        seed_colors.append(8)
      else:
        seed_colors.append(2)
    
    # Initialize output grid with white.
    output_grid = np.zeros((rows, output_cols), dtype=int)
    
    # determine the offset
    offset = 0
    for c in range(cols):
        found = False
        for r in range(rows):
            if input_grid[r,c] != 0:
                offset = c
                found = True
                break
        if found:
            break
    
    
    # Create the checkerboard pattern.
    color_index = 0
    for r in range(rows):
        for c in range(offset, output_cols):
            output_grid[r, c] = seed_colors[color_index % 2]
            color_index += 1
        color_index = (offset + r +1 )% 2 #offset the starting color for next row based on row index
    
    return output_grid.tolist()
```
