# f8a8fe49 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate the connected red (2) pixels forming a closed shape.  Also identify the individual grey (5) pixels.
2.  **Determine Axis:** Find the vertical center line of the red shape by finding bounding box.
3.  **Mirror Grey Pixels:** For each grey pixel inside the red shape consider a reflection across the local vertical center.
    *   If a grey pixel is *x* units to the *left* of the axis, move it to *x* units to the *right* of the axis.
    *   If a grey pixel is *x* units to the *right* of the axis, move it to *x* units to the *left* of the axis.
    *   If a grey pixel is *on* the axis, the grey pixel is moved to the other adjacent location.
4. **Preserve red shape:** Maintain the red pixels shape from the input.
5.  **Background:** Leave all other pixels as white (0).
"""

import numpy as np

def find_connected_components(grid, color):
    """Finds connected components of a specific color in the grid."""
    visited = set()
    components = []

    def dfs(r, c, component):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        component.append((r, c))
        dfs(r + 1, c, component)
        dfs(r - 1, c, component)
        dfs(r, c + 1, component)
        dfs(r, c - 1, component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                component = []
                dfs(r, c, component)
                components.append(component)
    return components

def bounding_box(component):
    """Calculates the bounding box of a component."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in component:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find red shape
    red_components = find_connected_components(input_grid, 2)
    if not red_components:
        return output_grid  # No red shape found
    
    red_shape = red_components[0] #expect only one

    # copy red pixels
    for r, c in red_shape:
      output_grid[r,c] = 2
    
    # Find grey pixels
    grey_pixels = [(r, c) for r in range(input_grid.shape[0]) for c in range(input_grid.shape[1]) if input_grid[r, c] == 5]

    # Determine axis: vertical center line of the bounding box
    min_r, min_c, max_r, max_c = bounding_box(red_shape)
    center_c = (min_c + max_c) / 2

    # Mirror grey pixels
    for r, c in grey_pixels:
        dist = c - center_c
        new_c = int(center_c - dist)

        
        # Check if new position is within bounds and place the mirrored pixel.
        if 0 <= new_c < output_grid.shape[1]:
            output_grid[r,new_c] = 5
        
    return output_grid
```
