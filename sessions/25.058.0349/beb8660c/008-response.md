# beb8660c • 008 • example_2 • investigate_coder

---
```python
"""
The transformation involves a specific vertical rearrangement of the rows containing the colored objects. It's a form of vertical shifting, where objects are maintaining their internal shape, but being moved down to be positioned as lowest as possible in the new array.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of non-background color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return []
        visited[r, c] = True
        object_pixels = [(r, c)]
        
        # Explore adjacent cells (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            object_pixels.extend(dfs(r + dr, c + dc, color))
        return object_pixels

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                objects.append(dfs(r, c, grid[r, c]))
    return objects

def transform(input_grid):
    """Transforms the input grid according to the rearrangement rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find the objects
    objects = find_objects(input_grid)

    # Create a list of rows to store the objects and their original row indices
    object_rows = []
    for obj in objects:
        # Get the row index of the object (using the first pixel)
        row_index = obj[0][0]
        object_rows.append((row_index, obj))


    # Sort based on original row_index from largest to smallest
    object_rows.sort(key=lambda item: item[0], reverse=True)

    #calculate new order of rows
    new_order = []
    empty_row_count = 0
    for i in range(rows):
        found = False
        for row_index, obj in object_rows:
            if row_index == i:
                new_order.append((row_index,obj))
                found = True
                break;
        if not found:
           empty_row_count+=1

    new_row_index = empty_row_count
    for row_index, obj in new_order:
        for r, c in obj:
            #shift = rows - 1 - row_index # original calcluation, but this assumes to always drop to bottom
            output_grid[new_row_index, c] = input_grid[r, c]
        new_row_index +=1
    
    return output_grid.tolist()
```
