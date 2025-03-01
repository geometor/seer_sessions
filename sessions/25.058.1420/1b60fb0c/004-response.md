# 1b60fb0c • 004 • example_1 • investigate_coder

---
```python
"""
Finds an enclosed area on the left side of a blue object in a grid and changes its color to red.
"""

import numpy as np

def find_blue_object(grid):
    # Find the coordinates of all blue (1) pixels.
    blue_pixels = np.argwhere(grid == 1)
    return blue_pixels

def find_enclosed_area(grid, blue_pixels):
    # Find boundaries by looking for changes in color.
    # We'll use a simple flood fill approach starting from the left
    
    if len(blue_pixels) == 0:
        return []
    
    min_y = np.min(blue_pixels[:, 0])
    min_x = np.min(blue_pixels[:, 1])

    #scan across from left
    start_pixel = None
    for x in range(grid.shape[1]):
      if grid[min_y,x] == 1:
          start_pixel = (min_y, x)
          break
    
    if not start_pixel:
        return []

    visited = set()
    queue = [start_pixel]
    enclosed_area = []
    
    #leftmost, not top
    while queue:
        y, x = queue.pop(0)

        if (y,x) in visited:
          continue
        
        visited.add((y, x))

        #if we see a 0 and we've visited a 1, we have left-most region
        if grid[y, x] == 0 and any(grid[v[0], v[1]]== 1 for v in visited):
          enclosed_area.append((y,x))
        
        #check valid neighbors, prioritize left
        neighbors = []
        if x > 0: 
            neighbors.append((y, x - 1))
        if y > 0:
            neighbors.append((y - 1, x))
        if x < grid.shape[1] - 1:
            neighbors.append((y, x + 1))
        if y < grid.shape[0] - 1:
            neighbors.append((y + 1, x))
    
    
        for neighbor in neighbors:
              if neighbor not in visited:
                queue.append(neighbor)

    return enclosed_area

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the blue object's pixels.
    blue_pixels = find_blue_object(output_grid)

    # Find the enclosed area
    enclosed = find_enclosed_area(output_grid, blue_pixels)
    
    #fill in enclosed area
    for y, x in enclosed:
      output_grid[y,x] = 2
    
    # debug
    # print(enclosed)
    
    return output_grid
```
