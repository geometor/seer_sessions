# be94b721 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Scan the input grid and identify all distinct contiguous rectangular regions of the same color.
2.  **Calculate Areas:** Determine the area (number of pixels) of each identified object.
3.  **Select Largest:** Find the object with the largest area.
4.  **Extract:** Create a new grid, copying only the pixels of the largest object, preserving its shape and relative position.
5.  **Isolate and output**: set every cell not part of the identified object in the new grid to 0 (white), the output grid shows only the largest object.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                current_object = []
                dfs(r, c, grid[r][c], current_object)
                if current_object:
                  # Check if it's rectangular
                  coords = np.array(current_object)
                  min_r, min_c = coords.min(axis=0)
                  max_r, max_c = coords.max(axis=0)
                  if len(current_object) == (max_r - min_r + 1) * (max_c - min_c + 1):
                    objects.append((current_object, grid[r][c]))
    return objects

def get_object_area(obj):
  """calculate the area of the object"""
  return len(obj)
    

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Find all objects
    objects = find_objects(input_grid)

    # Calculate areas and find the largest object
    largest_object = None
    max_area = 0
    for obj, color in objects:
        area = get_object_area(obj)
        if area > max_area:
            max_area = area
            largest_object = (obj, color)

    # initialize output grid
    output_grid = np.zeros((len(input_grid),len(input_grid[0])), dtype=int)


    # change output pixels
    if largest_object:
      for r, c in largest_object[0]:
        output_grid[r][c] = largest_object[1]

    # find min and max row and col
    coords = np.array(largest_object[0])
    min_r, min_c = coords.min(axis=0)
    max_r, max_c = coords.max(axis=0)      

    # Create a new grid with extracted object
    extracted_grid = output_grid[min_r:max_r+1, min_c:max_c+1]

    return extracted_grid
```
