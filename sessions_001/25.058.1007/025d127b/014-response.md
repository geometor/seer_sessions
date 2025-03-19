# 025d127b • 014 • example_2 • investigate_coder

---
```python
"""
Identify a connected shape of azure (8) pixels within the input grid.  Preserve a specific part of the outer edge of the shape. Clear all other azure pixels to white (0).
"""

import numpy as np

def get_azure_shape(grid):
    """Finds the connected azure shape and returns its coordinates."""
    azure_pixels = np.argwhere(grid == 8)
    if azure_pixels.size == 0:
        return []

    # Create a set for easier membership checking and to avoid duplicates
    shape_coords = set()

    # Start with the first azure pixel found
    stack = [tuple(azure_pixels[0])]

    while stack:
        current_pixel = stack.pop()
        shape_coords.add(current_pixel)

        # Check neighbors (up, down, left, right)
        row, col = current_pixel
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if (0 <= neighbor_row < grid.shape[0] and
                0 <= neighbor_col < grid.shape[1] and
                grid[neighbor_row, neighbor_col] == 8 and
                (neighbor_row, neighbor_col) not in shape_coords):
                stack.append((neighbor_row, neighbor_col))
    return list(shape_coords)


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_shape_coords = get_azure_shape(output_grid)
    
    # If there's no azure shape, return the input grid as is
    if not azure_shape_coords:
      return output_grid

    # Create a set for quick lookup
    azure_set = set(azure_shape_coords)

    # Iterate through the azure pixels and apply the "preserve edge" rule.
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
          if (r,c) not in azure_set:
              continue
          #keep one, remove one approach          
          if (r >=1 and c>=1 and c < output_grid.shape[1]-2):
              if(output_grid[r,c] ==8):
                  output_grid[r-1,1] = 8  

    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
          if (r,c) not in azure_set:
            continue
          if (r >=1 and c>=1):
              if output_grid[r,c] == 8 and (r,c) != (r-1,1):
                  output_grid[r,c] = 0


    return output_grid
```
