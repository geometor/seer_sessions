# 1bfc4729 • 014 • refine_coder

---
```python
"""
Transforms an input grid by expanding blue (1) and yellow (4) pixels into regions. Blue pixels expand upwards and downwards to the edges of the grid. Yellow pixels expand upwards and downwards to the edges of the grid. If both blue and yellow pixels exist, the space between the original blue and yellow rows is black.
"""

import numpy as np

def find_pixels(grid, color_value):
    """Finds the coordinates of all pixels with a specific color value."""
    positions = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == color_value:
                positions.append((r, c))
    return positions

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)  # Initialize with black (0)
    
    blue_pixels = find_pixels(input_grid, 1)
    yellow_pixels = find_pixels(input_grid, 4)
    rows = input_grid.shape[0]

    # Blue Expansion
    if blue_pixels:
        for blue_pos in blue_pixels:
            # Upward and downward expansion
            for r in range(rows):
                output_grid[r, :] = 1
            
    # Yellow Expansion
    if yellow_pixels:
        for yellow_pos in yellow_pixels:
            # Downward and upward expansion
            for r in range(rows):
                output_grid[r, :] = 4

    # Handle blue and yellow together
    if blue_pixels and yellow_pixels:
        for blue_pos in blue_pixels:
          for yellow_pos in yellow_pixels:
            # Fill space between with black
            start_row = min(blue_pos[0], yellow_pos[0])
            end_row = max(blue_pos[0], yellow_pos[0])
            for r in range(start_row + 1, end_row):
                output_grid[r, :] = 0


    return output_grid
```
