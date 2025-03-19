# 54d82841 • 002 • example_3 • investigate_coder

---
```python
"""
Copies the input grid to the output grid. Then, it identifies contiguous colored regions (excluding white/0) in the input grid.
If there's one object, it places a single yellow pixel (color 4) in the center of the bottom row, offset slightly left if the grid width is even.
If there are two or more non-white objects, it places two yellow pixels in the last row, aligned horizontally with the x-coordinates of those objects.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous colored regions (objects) in the grid, excluding background (0)."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append(obj)
    return objects


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    # Add yellow object based on object count
    if len(objects) >= 1:
        
        # create a list to put the locations, so code is not repeated for 1 or more
        locations = []
        
        if len(objects) == 1: # one object case
            center_col = cols // 2
            if cols % 2 == 0:  # Even width, offset slightly left
                center_col -=1
            
            locations.append(center_col)
    
        
        elif len(objects) >= 2:   #two object case
             # pick first two
            for obj in objects[0:2]: # iterate through the first two
                min_col = min(cell[1] for cell in obj)
                max_col = max(cell[1] for cell in obj)
                
                # favor putting on the edge of the object, use x coordinate of object
                if(input_grid.shape[1]-1 == max_col) :
                     locations.append(max_col)
                else : # pick minimum by default
                   locations.append(min_col)

        # put the locations
        for location in locations:
            output_grid[rows - 1, location] = 4 # set to yellow

    return output_grid
```
