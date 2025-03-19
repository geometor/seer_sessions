# 7ddcd7ec • 010 • example_2 • investigate_coder

---
```python
"""
Identify a connected component of yellow (4) pixels in the input grid,
translate it diagonally downwards and to the right, and replicate the
translated component to the edges of the grid.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []  # Return empty list if no object of the color is found
    return coords

def translate_object(coords, row_shift, col_shift):
    # Translate coordinates by given row and column shifts.
    translated_coords = []
    for r, c in coords:
        translated_coords.append((r + row_shift, c + col_shift))
    return translated_coords

def replicate_to_edge(grid, coords):
    # Replicate object to bottom-right edge
    rows, cols = grid.shape
    replicated_coords = coords.copy()
    
    max_row = max(r for r, _ in coords)
    max_col = max(c for _, c in coords)
    
    current_row_shift = 1
    current_col_shift = 1
    
    while max_row + current_row_shift < rows and max_col + current_col_shift < cols:
        new_coords = translate_object(coords, current_row_shift, current_col_shift)
        for r, c in new_coords:
          if 0 <= r < rows and 0 <= c < cols:
            replicated_coords.append((r,c))

        current_row_shift += 1
        current_col_shift += 1
    return replicated_coords
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the yellow object (color 4).
    yellow_coords = find_object(input_grid, 4)

    if not yellow_coords:
      return output_grid

    # translate object
    translated_coords = translate_object(yellow_coords, 1, 1)
    
    # replicate the pattern to the edge
    replicated_coords = replicate_to_edge(output_grid, translated_coords)

    # set original yellow to white
    for r, c in yellow_coords:
      output_grid[r, c] = 0

    # set translated and replicated coords
    for r, c in replicated_coords:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          output_grid[r, c] = 4

    return output_grid
```
