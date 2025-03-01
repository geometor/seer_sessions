# 6855a6e4 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies red (2) "C" shapes and repositions gray (5) pixels within the horizontal bounds of the red shapes to form a horizontal line.
"""

import numpy as np

def find_objects(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def get_horizontal_bounds(coords):
    """Gets the minimum and maximum x-coordinates from a set of coordinates."""
    if len(coords) == 0:
        return None, None
    return np.min(coords[:, 1]), np.max(coords[:, 1])

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    
    # Find red and gray objects
    red_coords = find_objects(input_grid, 2)
    gray_coords = find_objects(input_grid, 5)

    # Determine horizontal bounds of the red shapes
    min_x, max_x = get_horizontal_bounds(red_coords)
    if min_x is None or max_x is None:
        return output_grid # Return original if red is missing.

    # find vertical center
    min_y, max_y = np.min(red_coords[:, 0]), np.max(red_coords[:, 0])
    vertical_center = (min_y + max_y) // 2

    # Filter gray pixels within the horizontal bounds and clear them from output.
    relevant_gray_coords = []
    for y, x in gray_coords:
        if min_x < x < max_x:
            relevant_gray_coords.append((y,x))
        output_grid[y,x] = 0

    # Reposition gray pixels to form a horizontal line at center.
    if relevant_gray_coords:
        #find the y coordinate
      
        for x in range(min_x + 1, max_x):
             output_grid[vertical_center, x] = 5

    return output_grid
```
