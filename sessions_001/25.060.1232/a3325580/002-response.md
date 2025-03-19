# a3325580 • 002 • example_6 • investigate_coder

---
```python
"""
The transformation identifies non-background (non-zero) colors in the input grid.
The output grid contains columns representing each identified color.
The height of the output grid is determined by a complex relationship between
the number of objects and the number of rows each object spans.
"""

import numpy as np

def get_objects(grid):
    """
    Finds connected components (objects) in the grid.

    Returns a list of objects.  Each element of list is a
    list of (row,col) tuples of the non-background pixels.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    objects = get_objects(input_grid)

    # find distinct non zero colors
    colors = sorted(list(set(input_grid.flatten())))
    colors = [c for c in colors if c!= 0]

    # count the number of times each color appears
    num_rows = 0
    for obj in objects:
        num_rows = max(num_rows,len(obj))

    num_rows = 0
    first_color = -1
    for obj in objects:
        obj_color = input_grid[obj[0]]
        if first_color == -1:
             first_color = obj_color

        # we now know that objects may have dups across a single axis
        if obj_color == first_color:
            num_rows += 1

    output_grid = np.zeros((num_rows, len(colors)), dtype=int)

    # change output pixels
    for i in range(num_rows):
        for j, color in enumerate(colors):
          output_grid[i,j] = color

    return output_grid.tolist()
```
