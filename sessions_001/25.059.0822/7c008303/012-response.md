# 7c008303 • 012 • refine_coder

---
```python
"""
The transformation extracts specific color blocks (blue, red, and yellow) from the input grid and places them into the output grid. The selection criteria are based on adjacency: blue and red are selected together if adjacent, and yellow is selected if adjacent to blue. Azure and green objects are always removed. The output grid size is determined by a bounding box around selected objects, plus one row/col on top and left, and filled with black.
"""

import numpy as np

def find_objects(grid, colors):
    """Find objects of specified colors in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] in colors:
                obj = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj.append((curr_r, curr_c))

                    neighbors = [
                        (curr_r - 1, curr_c),
                        (curr_r + 1, curr_c),
                        (curr_r, curr_c - 1),
                        (curr_r, curr_c + 1),
                    ]
                    for nr, nc in neighbors:
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and not visited[nr, nc]
                            and grid[nr, nc] == grid[r, c]
                        ):
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                objects.append(obj)
    return objects

def are_adjacent(object1, object2):
    """Checks if two objects are adjacent."""
    for r1, c1 in object1:
        for r2, c2 in object2:
            if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1 and (abs(r1-r2) + abs(c1-c2) == 1):
                return True
    return False

def get_bounding_box(objects):
    """Calculates the bounding box for a list of objects."""
    if not objects:
        return (0, 0, 0, 0)

    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for obj in objects:
        for r, c in obj:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    return (min_r, min_c, max_r, max_c)

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Objects
    blue_objects = find_objects(input_grid, [1])
    red_objects = find_objects(input_grid, [2])
    yellow_objects = find_objects(input_grid, [4])

    # 2. Select Objects
    selected_blue = []
    selected_red = []
    selected_yellow = []

    for blue_obj in blue_objects:
        for red_obj in red_objects:
            if are_adjacent(blue_obj, red_obj):
                selected_blue = blue_obj
                selected_red = red_obj
                break  # Select only one blue/red pair
        if selected_blue:
            break

    for yellow_obj in yellow_objects:
      if selected_blue:
        if are_adjacent(yellow_obj, selected_blue):
            selected_yellow = yellow_obj
            break # Select only one

    # 3. Determine output grid size
    selected_objects = [selected_blue, selected_red, selected_yellow]
    selected_objects = [obj for obj in selected_objects if obj] # remove empty
    
    min_r, min_c, max_r, max_c = get_bounding_box(selected_objects)
    
    output_rows = max_r - min_r + 2
    output_cols = max_c - min_c + 2

    # 4. Initialize output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # calculate offset
    row_offset = 1 - min_r
    col_offset = 1 - min_c
    
    # 5. Position Selected Objects
    for r, c in selected_blue:
        output_grid[r + row_offset, c + col_offset] = 1
    for r, c in selected_red:
        output_grid[r + row_offset, c + col_offset] = 2
    for r, c in selected_yellow:
        output_grid[r + row_offset, c + col_offset] = 4


    return output_grid
```
