# f1cefba8 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Preserve the Blue Region:** The blue (1) pixels in the input grid mostly remain unchanged in the output grid.

2.  **Inner Yellow Modification:** The yellow (4) pixels inside of the continuous block defined by the blue pixels is changed, but only some of them. Yellow pixels are changed at coordinates with x value that is odd, to its horizontal neighbors value.

3.  **Outer Yellow border:** An outer yellow border is created, mirroring a single yellow pixel to each side of the blue shape, and replicating it on the top and bottom, vertically.
"""

import numpy as np

def find_objects(grid, color):
    # returns a list of coordinates of the target color
    objects = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
          if grid[r,c] == color:
            objects.append((r,c))
    return objects
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Preserve Blue Region
    # No explicit action needed as output_grid starts as a copy

    # Inner Yellow Modification
    yellow_pixels = find_objects(input_grid, 4)
    for r, c in yellow_pixels:
        if c % 2 == 1: # Odd column index
          if c > 0 and input_grid[r,c-1] == 1:
            output_grid[r, c] = 1  # Change to blue (neighbor value, if blue neighbor)
          elif c < cols -1 and input_grid[r,c+1] == 1:
             output_grid[r, c] = 1  # Change to blue

    # Outer Yellow border
    blue_pixels = find_objects(input_grid, 1)
    for r, c in blue_pixels:
      if c > 0 and input_grid[r, c-1] == 0:
        output_grid[r, c-1] = 4
      if c < cols -1 and input_grid[r, c+1] == 0:
        output_grid[r,c+1] = 4
      if r > 0 and input_grid[r-1,c] == 0:
        output_grid[r-1,c] = 4
      if r < rows - 1 and input_grid[r+1, c] == 0:
        output_grid[r+1,c] = 4
        
    return output_grid
```
