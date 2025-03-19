# eb5a1d5d • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to extract the central color of the largest
non-background object and place it in the center of a 3x3 grid filled with the
background color.
"""

import numpy as np

def find_largest_object(grid, background_color):
    # Find the largest contiguous object that is not the background color.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_size = 0
    max_object_coords = []

    def dfs(r, c, color, coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or
                grid[r, c] != color):
            return 0
        visited[r, c] = True
        coords.append((r, c))
        size = 1
        size += dfs(r + 1, c, color, coords)
        size += dfs(r - 1, c, color, coords)
        size += dfs(r, c + 1, color, coords)
        size += dfs(r, c - 1, color, coords)
        return size

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != background_color:
                coords = []
                size = dfs(r, c, grid[r, c], coords)
                if size > max_size:
                    max_size = size
                    max_object_coords = coords

    return max_object_coords

def find_object_center(coords):
     # Calculate the center (average) coordinates of an object.
    if not coords:
        return None
    rows, cols = zip(*coords)
    center_row = int(round(np.mean(rows)))
    center_col = int(round(np.mean(cols)))
    return center_row, center_col
    

def transform(input_grid):
    # Find background color (most frequent color)
    values, counts = np.unique(input_grid, return_counts=True)
    background_color = values[np.argmax(counts)]
    
    # Find largest object and its color
    largest_object_coords = find_largest_object(input_grid, background_color)
    if not largest_object_coords:
      object_color = background_color  #If not other objects, center will be background
    else:    
      object_color = input_grid[largest_object_coords[0]]

    # Find center
    center_row, center_col = find_object_center(largest_object_coords)
    
    
    # Create output grid
    output_grid = np.full((3, 3), background_color)

    # Place object color in the center of the output grid.
    output_grid[1, 1] = object_color

    return output_grid
```
