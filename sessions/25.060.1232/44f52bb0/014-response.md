# 44f52bb0 • 014 • refine_coder

---
```python
"""
The input grid contains a single object of color azure (8). The output grid is a blue (1) object whose dimensions are the transpose of the input object's dimensions.
"""

import numpy as np

def get_object(grid):
    """
    simple object detection - improved from describe_objects to return coords
    """
    # Convert grid to set of (color, (x,y)) tuples.
    pixels = {(color, (x, y)) for y, row in enumerate(grid) for x, color in enumerate(row)}
    objects = {}
    
    # Group contiguous pixels of same color by flood-fill procedure
    while pixels:
      color, (x,y) = pixels.pop()
      if color not in objects:
        objects[color] = []
      
      stack = [(x,y)]
      
      while stack:
        x,y = stack.pop()
        
        objects[color].append((x,y))

        # check the 4 adjacent neighbors
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for nx, ny in neighbors:
            if (color, (nx, ny)) in pixels:
                pixels.remove((color, (nx, ny)))
                stack.append((nx, ny))

    return objects

def transform(input_grid):
    # Find the object in the grid
    objects = get_object(input_grid)

    # should only be 1 object in these examples
    if len(objects) != 1:
        raise ValueError("Expected exactly one object in input_grid")

    # the key will the color, get the coordinates
    coords = list(objects.values())[0]
    
    # Determine object dimensions
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Create output grid with transposed dimensions and filled with blue (1)
    output_grid = np.full((height, width), 1, dtype=int)

    return output_grid
```
