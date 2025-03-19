# aba27056 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation identifies the orange (7) shape in the input grid. It then traces a border around this shape. The border includes all orange pixels, and extends one pixel outwards wherever an orange pixel is adjacent to a white (0) background pixel. Finally, it fills all pixels inside and on the border with yellow (4).
"""

import numpy as np

def get_orange_shape(grid):
    # Find coordinates of all orange pixels
    return np.where(grid == 7)

def trace_border(grid, orange_coords):
    # Create a set for efficient checking of orange pixel locations
    orange_set = set(zip(orange_coords[0], orange_coords[1]))
    rows, cols = grid.shape
    border_coords = set()

    # Iterate through orange pixels
    for r, c in zip(*orange_coords):
        border_coords.add((r, c))  # Orange pixels are part of the border

        # Check neighbors for background pixels
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc
                # if neighbor valid
                if 0 <= nr < rows and 0 <= nc < cols:
                  # if neighbor is background, expand one position further
                  if grid[nr, nc] == 0:
                      extr, extc = r + 2*dr, c+ 2*dc

                      # check boundaries of extended
                      if 0 <= extr < rows and 0 <= extc < cols:
                        border_coords.add((extr, extc))


    return border_coords

def fill_border(grid, border_coords):
  output_grid = grid.copy()

  # get min and max of rows
  min_row = min(border_coords, key=lambda x: x[0])[0]
  max_row = max(border_coords, key=lambda x: x[0])[0]

  # get min and max of cols
  min_col = min(border_coords, key=lambda x: x[1])[1]
  max_col = max(border_coords, key=lambda x: x[1])[1]
  
  # fill from top left
  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
        output_grid[r, c] = 4  # Fill with yellow

  return output_grid

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = input_grid.copy()

    # Get coordinates of the orange shape
    orange_coords = get_orange_shape(input_grid)

    # Trace the border around the orange shape
    border_coords = trace_border(input_grid, orange_coords)

    # Fill the area within and including the border with yellow
    output_grid = fill_border(output_grid, border_coords)
    
    # replace the orange pixels with yellow
    for r,c in zip(orange_coords[0], orange_coords[1]):
      output_grid[r,c] = 4


    return output_grid
```
